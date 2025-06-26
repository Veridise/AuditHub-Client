#!/usr/bin/env python3
import logging
from dataclasses import dataclass
from typing import Literal, Optional

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import POST
from ..library.net_utils import ensure_success, response_json
from ..library.utils import get_dict_of_fields_except

logger = logging.getLogger(__name__)


@dataclass
class StartVanguardTaskArgs:
    organization_id: int
    project_id: int
    version_id: int
    name: Optional[str]
    detector: list[str]
    input_limit: Optional[list[str]]
    tool_name: Literal["vanguard", "vanguard-v2", "zk-vanguard"]


def api_start_vanguard_task(context: AuditHubContext, input: StartVanguardTaskArgs):
    logger.debug("Starting Vanguard")

    data = {
        "name": input.name,
        "parameters": get_dict_of_fields_except(
            input, {"organization_id", "project_id", "version_id", "name", "tool_name"}
        ),
    }
    logger.debug("Posting data: %s", data)

    response = authentication_retry(
        context,
        POST,
        url=f"{context.base_url}/organizations/{input.organization_id}/projects/{input.project_id}/versions/{input.version_id}/tools/{input.tool_name}",
        json=data,
    )
    ensure_success(response)
    ret = response_json(response)
    return ret
