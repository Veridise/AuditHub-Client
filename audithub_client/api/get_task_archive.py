#!/usr/bin/env python3
from dataclasses import dataclass

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import GET
from ..library.net_utils import Downloader


@dataclass
class GetTaskArchiveArgs:
    organization_id: int
    task_id: int


def api_get_task_archive(
    context: AuditHubContext, input: GetTaskArchiveArgs, downloader: Downloader
):
    response = authentication_retry(
        context,
        GET,
        url=f"{context.base_url}/organizations/{input.organization_id}/tasks/{input.task_id}/archive",
        downloader=downloader,
    )
    return response
