#!/usr/bin/env python3
from dataclasses import dataclass

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import GET
from ..library.net_utils import ensure_success, response_json


@dataclass
class GetLatestVersionArgs:
    organization_id: int
    project_id: int


def api_get_latest_version(
    context: AuditHubContext, input: GetLatestVersionArgs
) -> dict:
    response = authentication_retry(
        context,
        GET,
        url=f"{context.base_url}/organizations/{input.organization_id}/projects/{input.project_id}/versions/latest",
    )
    ensure_success(response)
    ret = response_json(response)
    return ret
