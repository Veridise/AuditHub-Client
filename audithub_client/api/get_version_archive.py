#!/usr/bin/env python3
from dataclasses import dataclass

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import GET
from ..library.net_utils import Downloader


@dataclass
class GetVersionArchiveArgs:
    organization_id: int
    project_id: int
    version_id: int


def api_get_version_archive(
    context: AuditHubContext, input: GetVersionArchiveArgs, downloader: Downloader
):
    response = authentication_retry(
        context,
        GET,
        url=f"{context.base_url}/organizations/{input.organization_id}/projects/{input.project_id}/versions/{input.version_id}/archive",
        downloader=downloader,
    )
    return response
