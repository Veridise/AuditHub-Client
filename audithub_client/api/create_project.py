#!/usr/bin/env python3
from dataclasses import dataclass

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import POST
from ..library.net_utils import ensure_success, response_json
from .models import ProjectInfo


@dataclass
class CreateProjectArgs:
    organization_id: int
    project_definition: ProjectInfo
    temp_version_id: int | None


def api_create_project(context: AuditHubContext, input: CreateProjectArgs) -> dict:
    params = {}
    if input.temp_version_id:
        params["temp_version_id"] = input.temp_version_id
    response = authentication_retry(
        context,
        POST,
        url=f"{context.base_url}/organizations/{input.organization_id}/projects",
        json=input.project_definition.model_dump(),
        params=params,
    )
    ensure_success(response)
    ret = response_json(response)
    return ret
