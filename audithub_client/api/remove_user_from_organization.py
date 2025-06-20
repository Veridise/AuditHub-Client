#!/usr/bin/env python3

from dataclasses import dataclass

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import DELETE
from ..library.net_utils import ensure_success, response_json


@dataclass
class RemoveUserFromOrganizationArgs:
    organization_id: int
    user_id: str


def api_remove_user_from_organization(
    context: AuditHubContext, input: RemoveUserFromOrganizationArgs
):
    response = authentication_retry(
        context,
        DELETE,
        url=f"{context.base_url}/organizations/{input.organization_id}/users/{input.user_id}",
    )
    # response.raise_for_status()
    ensure_success(response)
    return response_json(response)
