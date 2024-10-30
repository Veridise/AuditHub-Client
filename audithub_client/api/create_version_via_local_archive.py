#!/usr/bin/env python3
from dataclasses import dataclass
from pathlib import Path

from requests import post

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.net_utils import ensure_success, response_json


@dataclass
class CreateVersionViaLocalArchiveArgs:
    organization_id: int
    project_id: int
    name: str
    archive_path: Path


def api_create_version_via_local_archive(
    context: AuditHubContext, input: CreateVersionViaLocalArchiveArgs
):
    with input.archive_path.open("rb") as fp:
        data = {"name": input.name}

        response = authentication_retry(
            context,
            post,
            url=f"{context.base_url}/organizations/{input.organization_id}/projects/{input.project_id}/versions",
            data=data,
            files={"archive": ("sources.zip", fp, "application/zip")},
        )
        ensure_success(response)
        ret = response_json(response)
        return ret
