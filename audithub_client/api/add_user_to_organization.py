#!/usr/bin/env python3
from dataclasses import dataclass

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import POST
from ..library.net_utils import ensure_success, response_json
from ..library.utils import get_dict_of_fields_except


@dataclass
class AddUserToOrganizationArgs:
    organization_id: int
    user_id: str


def api_add_user_to_organization(
    context: AuditHubContext, input: AddUserToOrganizationArgs
):
    data = get_dict_of_fields_except(input, {"organization_id"})
    response = authentication_retry(
        context,
        POST,
        url=f"{context.base_url}/organizations/{input.organization_id}/users",
        json=data,
    )
    ensure_success(response)
    ret = response_json(response)
    return ret
