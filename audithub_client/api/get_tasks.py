#!/usr/bin/env python3
from dataclasses import asdict, dataclass
from datetime import datetime

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import GET
from ..library.net_utils import ensure_success, response_json


@dataclass
class GetTasksArgs:
    organization_id: int
    project_id: int | None = None
    version_id: int | None = None
    from_created_at: datetime | None = None
    to_created_at: datetime | None = None
    limit: int | None = None
    offset: int | None = None
    order_by: str | None = None


def api_get_tasks(context: AuditHubContext, input: GetTasksArgs):
    params = {
        key: value
        for key, value in asdict(input).items()
        if key != "organization_id" and value is not None
    }
    response = authentication_retry(
        context,
        GET,
        url=f"{context.base_url}/organizations/{input.organization_id}/tasks",
        params=params,
    )
    ensure_success(response)
    ret = response_json(response)
    return ret
