#!/usr/bin/env python3
from dataclasses import dataclass

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import get
from ..library.net_utils import ensure_success


@dataclass
class GetTaskArchiveArgs:
    organization_id: int
    task_id: int


def api_get_task_archive(context: AuditHubContext, input: GetTaskArchiveArgs):
    response = authentication_retry(
        context,
        get,
        url=f"{context.base_url}/organizations/{input.organization_id}/tasks/{input.task_id}/archive",
        stream=True,
    )
    ensure_success(response)
    return response
