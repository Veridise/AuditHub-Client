import json
import logging
import time
from typing import Callable, Optional

from httpx import Client, Timeout, get, post

from audithub_client.library.net_utils import Downloader

from .context import AuditHubContext
from .http import Response

AUTHENTICATION_TIMEOUT = Timeout(connect=10, read=30, write=30, pool=10)
DEFAULT_REQUEST_TIMEOUT = Timeout(connect=10, read=90, write=600, pool=10)
logger = logging.getLogger(__name__)


def get_access_token(
    rpc_context: AuditHubContext,
    token_time_listener: Optional[Callable[[float], None]] = None,
) -> str:
    begin_time = time.perf_counter()
    logger.debug(
        "Obtaining IdP configuration from %s", rpc_context.oidc_configuration_url
    )
    response = get(rpc_context.oidc_configuration_url, timeout=AUTHENTICATION_TIMEOUT)
    token_url = response.json()["token_endpoint"]
    logger.debug("Obtaining IdP token from %s", token_url)
    payload = {
        "client_id": rpc_context.oidc_client_id,
        "client_secret": rpc_context.oidc_client_secret,
        "scope": "openid profile",
        "grant_type": "client_credentials",
    }
    # logger.debug("Payload is %s", payload)
    response = post(token_url, data=payload, timeout=AUTHENTICATION_TIMEOUT)
    if response.status_code != 200:
        raise RuntimeError(
            f'Failed to get token for client {payload["client_id"]} status = {response.status_code} response ={response.text}'
        )
    token_data = response.json()
    end_time = time.perf_counter()
    logger.debug(json.dumps(token_data))
    if token_time_listener:
        token_time_listener(end_time - begin_time)
    return token_data["access_token"]


def get_token_header(access_token):
    return {"Authorization": f"Bearer {access_token}"}


def authentication_retry(
    rpc_context: AuditHubContext,
    http_method: str,
    retries=1,
    request_timeout: Timeout | None = None,
    downloader: Downloader | None = None,
    token_time_listener: Optional[Callable[[float], None]] = None,
    **kwargs,
) -> Response:
    if request_timeout is None:
        request_timeout = DEFAULT_REQUEST_TIMEOUT
    # access_token is stored as an attribute of this function
    if not hasattr(authentication_retry, "access_token"):
        # if not found, it is created
        authentication_retry.access_token = get_access_token(rpc_context, token_time_listener)  # type: ignore
    with Client(timeout=request_timeout) as client:
        while retries >= 0:
            if downloader:
                with client.stream(
                    http_method,
                    headers=get_token_header(authentication_retry.access_token),  # type: ignore
                    timeout=request_timeout,
                    **kwargs,
                ) as response:
                    if response.status_code == 401:
                        # if auth_token expired, obtain a new one
                        authentication_retry.access_token = get_access_token(rpc_context, token_time_listener)  # type: ignore
                        retries = retries - 1
                    else:
                        downloader.download(response)
                        return response
            else:
                response = client.request(
                    method=http_method,
                    headers=get_token_header(authentication_retry.access_token),  # type: ignore
                    timeout=request_timeout,
                    **kwargs,
                )
                if response.status_code == 401:
                    # if auth_token expired, obtain a new one
                    authentication_retry.access_token = get_access_token(rpc_context, token_time_listener)  # type: ignore
                    retries = retries - 1
                else:
                    return response
        return response


def reset_authentication():
    if hasattr(authentication_retry, "access_token"):
        delattr(authentication_retry, "access_token")
