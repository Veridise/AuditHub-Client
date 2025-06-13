#!/usr/bin/env python3
from dataclasses import dataclass

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import get
from ..library.net_utils import ensure_success


@dataclass
class GetTaskArtifactArgs:
    organization_id: int
    task_id: int
    artifact_id: int


def api_get_artifact(context: AuditHubContext, input: GetTaskArtifactArgs):
    response = authentication_retry(
        context,
        get,
        url=f"{context.base_url}/organizations/{input.organization_id}/tasks/{input.task_id}/artifacts/{input.artifact_id}",
        stream=True,
    )
    ensure_success(response)
    return response
