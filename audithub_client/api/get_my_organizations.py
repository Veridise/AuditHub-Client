#!/usr/bin/env python3

from requests import get

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.net_utils import ensure_success, response_json


def api_get_my_organizations(context: AuditHubContext):
    response = authentication_retry(
        context, get, url=f"{context.base_url}/users/myorganizations"
    )
    ensure_success(response)
    return response_json(response)
