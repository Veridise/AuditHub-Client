#!/usr/bin/env python3

from dataclasses import dataclass

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import GET
from ..library.net_utils import ensure_success, response_json


@dataclass
class GetOrganizationRestrictionsArgs:
    id: int


def api_get_organization_restrictions(
    context: AuditHubContext, input: GetOrganizationRestrictionsArgs
):
    response = authentication_retry(
        context, GET, url=f"{context.base_url}/organizations/{input.id}/restrictions"
    )
    ensure_success(response)
    return response_json(response)
