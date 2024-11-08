import json
import logging
import time
from typing import Callable, Optional

from requests import Response, get, post

from .context import AuditHubContext

RESPONSE_TIMEOUT = 90
logger = logging.getLogger(__name__)


def get_access_token(
    rpc_context: AuditHubContext,
    token_time_listener: Optional[Callable[[float], None]] = None,
) -> str:
    begin_time = time.perf_counter()
    logger.debug(
        "Obtaining IdP configuration from %s", rpc_context.oidc_configuration_url
    )
    response = get(rpc_context.oidc_configuration_url, timeout=RESPONSE_TIMEOUT)
    token_url = response.json()["token_endpoint"]
    logger.debug("Obtaining IdP token from %s", token_url)
    payload = {
        "client_id": rpc_context.oidc_client_id,
        "client_secret": rpc_context.oidc_client_secret,
        "scope": "openid profile",
        "grant_type": "client_credentials",
    }
    logger.debug("Payload is %s", payload)
    response = post(token_url, data=payload, timeout=RESPONSE_TIMEOUT)
    if response.status_code != 200:
        raise RuntimeError(
            f'Failed to get token for client {payload["client_id"]} status = {response.status_code} response ={response.text}'
        )
    token_data = response.json()
    end_time = time.perf_counter()
    logger.debug(json.dumps(token_data, indent=4))
    if token_time_listener:
        token_time_listener(end_time - begin_time)
    return token_data["access_token"]


def get_token_header(access_token):
    return {"Authorization": f"Bearer {access_token}"}


def authentication_retry(
    rpc_context: AuditHubContext,
    http_method,
    retries=1,
    token_time_listener: Optional[Callable[[float], None]] = None,
    **kwargs,
) -> Response:
    # access_token is stored as an attribute of this function
    if not hasattr(authentication_retry, "access_token"):
        # if not found, it is created
        authentication_retry.access_token = get_access_token(rpc_context, token_time_listener)  # type: ignore
    while retries >= 0:
        response = http_method(
            headers=get_token_header(authentication_retry.access_token),  # type: ignore
            timeout=RESPONSE_TIMEOUT,
            **kwargs,
        )
        if response.status_code == 401:
            # if auth_token expired, obtain a new one
            authentication_retry.access_token = get_access_token(token_time_listener)  # type: ignore
            retries = retries - 1
        else:
            return response
    return response


def reset_authentication():
    if hasattr(authentication_retry, "access_token"):
        delattr(authentication_retry, "access_token")
