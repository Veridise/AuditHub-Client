#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Literal, Optional

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import POST
from ..library.net_utils import ensure_success, response_json
from ..library.utils import get_dict_of_fields_except


@dataclass
class CreateVersionViaUrlArgs:
    organization_id: int
    project_id: int
    name: str
    input_type: Literal["git", "archive"]
    url: str
    revision: Optional[str] = None
    includes_submodules: Optional[bool] = None


def api_create_version_via_url(
    context: AuditHubContext, input: CreateVersionViaUrlArgs
):
    data = get_dict_of_fields_except(input, {"organization_id", "project_id"})

    response = authentication_retry(
        context,
        POST,
        url=f"{context.base_url}/organizations/{input.organization_id}/projects/{input.project_id}/versions-url",
        data=data,
    )
    ensure_success(response)
    ret = response_json(response)
    return ret
