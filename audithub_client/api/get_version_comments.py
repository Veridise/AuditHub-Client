#!/usr/bin/env python3
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from audithub_client.library.utils import get_dict_of_fields_except

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import GET
from ..library.net_utils import ensure_success, response_json


@dataclass
class GetVersionCommentsArgs:
    organization_id: int
    project_id: int
    version_id: int
    thread_id: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


@dataclass
class CommentMessage:
    project_id: int
    thread_id: int
    data: Optional[str]
    id: int
    created_at: datetime
    created_by: str
    is_modified: bool
    is_deleted: bool
    version_id: Optional[int] = None
    system_generated: Optional[bool] = None


def api_get_version_comments(
    context: AuditHubContext, input: GetVersionCommentsArgs
) -> list[CommentMessage]:

    query_params = get_dict_of_fields_except(
        input, {"organization_id", "project_id", "version_id"}
    )

    response = authentication_retry(
        context,
        GET,
        url=f"{context.base_url}/organizations/{input.organization_id}/projects/{input.project_id}/versions/{input.version_id}/comments",
        params=query_params,
    )
    ensure_success(response)
    ret = response_json(response)
    return ret
