#!/usr/bin/env python3
from dataclasses import dataclass

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import GET
from ..library.net_utils import ensure_success, response_json


@dataclass
class GetTaskLogsArgs:
    organization_id: int
    task_id: int
    step_code: str


def api_get_task_logs(context: AuditHubContext, input: GetTaskLogsArgs):
    response = authentication_retry(
        context,
        GET,
        url=f"{context.base_url}/organizations/{input.organization_id}/tasks/{input.task_id}/{input.step_code}/output",
    )
    ensure_success(response)
    ret = response_json(response)
    return ret
