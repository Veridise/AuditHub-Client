#!/usr/bin/env python3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import GET
from ..library.net_utils import ensure_success, response_json


@dataclass
class SendDigestNotificationsArgs:
    user_id: Optional[str]
    days_to_include: Optional[int]


def get_query_timestamp(days_to_include: int):
    return (datetime.now(timezone.utc) - timedelta(days=days_to_include)).isoformat()


def api_send_digest_notifications(
    context: AuditHubContext, input: SendDigestNotificationsArgs
):

    query_params = {}
    if input.user_id:
        query_params["user_id"] = input.user_id
    if input.days_to_include:
        query_params["from_created_at"] = get_query_timestamp(input.days_to_include)

    response = authentication_retry(
        context, GET, url=f"{context.base_url}/admin/digest", params=query_params
    )
    ensure_success(response)
    ret = response_json(response)
    return ret
