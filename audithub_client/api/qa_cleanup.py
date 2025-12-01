#!/usr/bin/env python3

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import DEFAULT_CONNECT_TIMEOUT, DEFAULT_POOL_TIMEOUT, GET, Timeout
from ..library.net_utils import ensure_success, response_json


def api_qa_cleanup(context: AuditHubContext):
    response = authentication_retry(
        context,
        GET,
        url=f"{context.base_url}/admin/qa-cleanup",
        request_timeout=Timeout(
            connect=DEFAULT_CONNECT_TIMEOUT,
            read=900,
            write=30,
            pool=DEFAULT_POOL_TIMEOUT,
        ),
    )
    response.raise_for_status()
    ensure_success(response)
    return response_json(response)
