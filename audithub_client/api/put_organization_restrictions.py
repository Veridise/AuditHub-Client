#!/usr/bin/env python3
from dataclasses import dataclass

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import PUT
from ..library.net_utils import ensure_success, response_json
from .models import OrganizationAccessRestrictions


@dataclass
class PutOrganizationRestrictionsArgs:
    organization_id: int
    restrictions: OrganizationAccessRestrictions


def api_put_organization_restrictions(
    context: AuditHubContext, input: PutOrganizationRestrictionsArgs
) -> dict:
    response = authentication_retry(
        context,
        PUT,
        url=f"{context.base_url}/organizations/{input.organization_id}/restrictions",
        json=input.restrictions.model_dump(),
    )
    ensure_success(response)
    ret = response_json(response)
    return ret
