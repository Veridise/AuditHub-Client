#!/usr/bin/env python3
from dataclasses import asdict, dataclass
from typing import Optional

from requests import post

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.net_utils import ensure_success, response_json


@dataclass
class CreateOrganizationArgs:
    name: str
    support_channel: Optional[str] = None


def api_add_user_to_organization(
    context: AuditHubContext, input: CreateOrganizationArgs
):
    data = asdict(input)
    response = authentication_retry(
        context,
        post,
        url=f"{context.base_url}/organizations",
        json=data,
    )
    ensure_success(response)
    ret = response_json(response)
    return ret
