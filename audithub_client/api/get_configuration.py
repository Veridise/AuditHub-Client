#!/usr/bin/env python3

from ..library.context import AuditHubContext
from ..library.http import get
from ..library.net_utils import ensure_success, response_json


def api_get_configuration(context: AuditHubContext):
    response = get(url=f"{context.base_url}/configuration")
    ensure_success(response)
    return response_json(response)
