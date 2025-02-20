#!/usr/bin/env python3
from dataclasses import dataclass

from requests import delete

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.net_utils import ensure_success, response_json


@dataclass
class DeleteOrganizationArgs:
    id: int


def api_delete_organization(context: AuditHubContext, input: DeleteOrganizationArgs):
    response = authentication_retry(
        context,
        delete,
        url=f"{context.base_url}/organizations/{input.id}",
    )
    ensure_success(response)
    ret = response_json(response)
    return ret
