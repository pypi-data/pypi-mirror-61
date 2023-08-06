import os
import time
from typing import Dict

from cohesivenet import (
    VNS3Client,
    data_types,
    CohesiveSDKException,
    ApiException,
    Logger,
    UrlLib3ConnExceptions,
    HTTPStatus,
)
from cohesivenet.macros import api_operations


def fetch_keyset_from_source(client, source, token, wait_timeout=180.0):
    """fetch_keyset_from_source Put keyset by providing source controller to download keyset. This
    contains logic that handles whether or not fetching from the source fails, typically due
    to a firewall or routing issue in the underlay network (e.g. security groups and route tables).

    Pseudo-logic:
        PUT new keyset request to fetch from remote controller
        if keyset exists or already in progress, fail immediately as its unexpected
        if PUT succees:
            wait:
                if a new successful put returns: that indicates failure to download from source. return 400
                if timeout: that indicates controller is rebooting, return wait for keyset
                if keyset already exists, wait to ensure keyset  exists, then return keyset details

    Arguments:
        source {str} - host controller to fetch keyset from
        token {str} - secret token used when generating keyset
        wait_timeout {float} - timeout for waiting for keyset and while polling for download failure (default: 1 min)

    Raises:
        e: ApiException or CohesiveSDKException

    Returns:
        KeysetDetail
    """
    sleep_time = 2.0
    failure_error_str = (
        "Failed to fetch keyset for source. This typically due to a misconfigured "
        "firewall or routing issue between source and client controllers."
    )

    try:
        put_response = client.config.put_keyset({"source": source, "token": token})
    except ApiException as e:
        Logger.info(
            "Failed to fetch keyset: %s" % e.get_error_message(), host=client.host_uri,
        )
        raise e
    except UrlLib3ConnExceptions:
        raise ApiException(
            status=HTTPStatus.SERVICE_UNAVAILABLE,
            reason="Controller unavailable. It is likely rebooting. Try client.sys_admin.wait_for_api().",
        )

    if not put_response.response:
        keyset_data = client.config.get_keyset()
        if keyset_data.response and keyset_data.response.keyset_present:
            raise ApiException(status=400, reason="Keyset already exists.")
        raise ApiException(status=500, reason="Put keyset returned None.")

    start_time = put_response.response.started_at_i
    Logger.info(message="Keyset downloading from source.", start_time=start_time)
    polling_start = time.time()
    while time.time() - polling_start <= wait_timeout:
        try:
            duplicate_call_resp = client.config.put_keyset(
                {"source": source, "token": token}
            )
        except UrlLib3ConnExceptions:
            Logger.info(
                "API call timeout. Controller is likely rebooting. Waiting for keyset.",
                wait_timeout=wait_timeout,
            )
            client.sys_admin.wait_for_api(timeout=wait_timeout, wait_for_reboot=True)
            return client.config.wait_for_keyset(timeout=wait_timeout)
        except ApiException as e:
            duplicate_call_error = e.get_error_message()

            if duplicate_call_error == "Keyset already exists.":
                keyset_data = client.config.try_get_keyset()
                if not keyset_data:
                    Logger.info(
                        "Keyset exists. Waiting for reboot.", wait_timeout=wait_timeout
                    )
                    client.sys_admin.wait_for_api(
                        timeout=wait_timeout, wait_for_reboot=True
                    )
                    return client.config.wait_for_keyset()
                return keyset_data

            if duplicate_call_error == "Keyset setup in progress.":
                # this means download is in progress, but might fail. Wait and retry
                time.sleep(sleep_time)
                continue

            # Unexpected ApiException
            raise e

        # If there is a new start time for keyset generation, that indicates a failure
        new_start_resp = duplicate_call_resp.response
        new_start = new_start_resp.started_at_i if new_start_resp else None
        if (new_start and start_time) and (new_start != start_time):
            Logger.error(failure_error_str, source=source)
            raise ApiException(status=HTTPStatus.BAD_REQUEST, reason=failure_error_str)

        time.sleep(sleep_time)
    raise CohesiveSDKException("Timeout while waiting for keyset.")


def setup_controller(
    client: VNS3Client,
    topology_name: str,
    license_file: str,
    license_parameters: Dict,
    keyset_parameters: Dict,
    peering_id: int = 1,
    reboot_timeout=120,
    keyset_timeout=120,
):
    """setup_controller Set the topology name, controller license, keyset and peering ID if provided

    Arguments:
        client {VNS3Client}
        topology_name {str}
        keyset_parameters {Dict} -- UpdateKeysetRequest {
            'source': 'str',
            'token': 'str',
            'topology_name': 'str',
            'sealed_network': 'bool'
        }
        peering_id {int} -- ID for this controller in peering mesh

    Returns:
        OperationResult
    """
    current_config = client.config.get_config().response
    Logger.info("Setting topology name", name=topology_name)
    if current_config.topology_name != topology_name:
        client.config.put_config({"topology_name": topology_name})

    if not current_config.licensed:
        if not os.path.isfile(license_file):
            raise CohesiveSDKException("License file does not exist")

        license_file_data = open(license_file).read().strip()
        Logger.info("Uploading license file", path=license_file)
        client.licensing.upload_license(license_file_data)

    accept_license = False
    try:
        current_license = client.licensing.get_license().response
        accept_license = not current_license or not current_license.finalized
    except ApiException as e:
        if e.get_error_message() == "Must be licensed first.":
            accept_license = True
        else:
            raise e

    if accept_license:
        Logger.info("Accepting license", parameters=license_parameters)
        client.licensing.put_set_license_parameters(license_parameters)
        Logger.info("Waiting for server reboot.")
        client.sys_admin.wait_for_api(timeout=reboot_timeout, wait_for_reboot=True)

    current_keyset = api_operations.retry_call(
        client.config.get_keyset, max_attempts=20
    ).response
    if not current_keyset.keyset_present and not current_keyset.in_progress:
        Logger.info("Generating keyset", parameters=keyset_parameters)
        api_operations.retry_call(client.config.put_keyset, args=(keyset_parameters,))
        Logger.info("Waiting for keyset ready")
        client.config.wait_for_keyset(timeout=keyset_timeout)
    elif current_keyset.in_progress:
        client.config.wait_for_keyset(timeout=keyset_timeout)

    current_peering_status = client.peering.get_peering_status().response
    if not current_peering_status.id and peering_id:
        Logger.info("Setting peering id", id=peering_id)
        client.peering.put_self_peering_id({"id": peering_id})
    return client


def license_clients(clients, license_file_path) -> data_types.BulkOperationResult:
    """Upload license file to all clients. These will have DIFFERENT keysets. See keyset operations
       if all controllers are to be in the same clientpack topology

    Arguments:
        clients {List[VNS3Client]}
        license_file_path {str} - full path to license file

    Returns:
        BulkOperationResult
    """
    license_file = open(license_file_path).read().strip()

    def _upload_license(_client):
        return _client.licensing.upload_license(license_file)

    return api_operations.__bulk_call_client(clients, _upload_license)


def accept_clients_license(
    clients, license_parameters
) -> data_types.BulkOperationResult:
    """Accept licenses for all. These will have DIFFERENT keysets. See keyset operations
       if all controllers are to be in the same clientpack topology. Assumes same license
       parameters will be accepted for all clients

    Arguments:
        clients {List[VNS3Client]}
        license_parameters {UpdateLicenseParametersRequest} - dict {
            'subnet': 'str',
            'managers': 'str',
            'asns': 'str',
            'clients': 'str',
            'my_manager_vip': 'str',
            'default': 'bool'
        }

    Returns:
        BulkOperationResult
    """

    def _accept_license(_client):
        return _client.licensing.put_set_license_parameters(license_parameters)

    return api_operations.__bulk_call_client(clients, _accept_license)


def fetch_keysets(clients, root_host, keyset_token, wait_timeout=80.0):
    """fetch_keysets Fetch keysets for all clients from root_host

    Arguments:
        clients {List[VNS3Client]}
        root_host {str}
        keyset_token {str}

    Returns:
        BulkOperationResult
    """

    def _fetch_keyset(_client):
        return fetch_keyset_from_source(
            _client, root_host, keyset_token, wait_timeout=wait_timeout
        )

    return api_operations.__bulk_call_client(clients, _fetch_keyset, parallelize=False)
