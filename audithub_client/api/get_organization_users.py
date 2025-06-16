#!/usr/bin/env python3

from dataclasses import dataclass

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import GET
from ..library.net_utils import ensure_success, response_json


@dataclass
class GetOrganizationUsersArgs:
    id: int


def api_get_organization_users(
    context: AuditHubContext, input: GetOrganizationUsersArgs
):
    response = authentication_retry(
        context, GET, url=f"{context.base_url}/organizations/{input.id}/users"
    )
    # response.raise_for_status()
    ensure_success(response)
    return response_json(response)
