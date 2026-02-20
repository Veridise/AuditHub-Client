#!/usr/bin/env python3

from dataclasses import dataclass

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import GET
from ..library.net_utils import ensure_success, response_json


@dataclass
class GetOrganizationProjectsArgs:
    id: int


def api_get_organization_projects(
    context: AuditHubContext, input: GetOrganizationProjectsArgs
):
    response = authentication_retry(
        context, GET, url=f"{context.base_url}/organizations/{input.id}/projects"
    )
    ensure_success(response)
    return response_json(response)
