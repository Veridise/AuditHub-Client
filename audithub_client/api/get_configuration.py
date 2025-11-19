#!/usr/bin/env python3

from ..library.context import AuditHubContext
from ..library.http import get
from ..library.net_utils import ensure_success, response_json
from ..library.ssl import get_verify_ssl


def api_get_configuration(context: AuditHubContext):
    url = f"{context.base_url}/configuration"
    response = get(url=url, verify=get_verify_ssl(url))
    ensure_success(response)
    return response_json(response)
