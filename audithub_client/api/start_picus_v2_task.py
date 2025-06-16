#!/usr/bin/env python3
import logging
from dataclasses import dataclass
from typing import Optional

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import POST
from ..library.net_utils import ensure_success, response_json
from ..library.utils import get_dict_of_fields_except

logger = logging.getLogger(__name__)


@dataclass
class StartPicusV2TaskArgs:
    organization_id: int
    project_id: int
    version_id: int
    name: Optional[str]
    source: str
    solver: Optional[str] = None
    solver_timeout: Optional[int] = None
    time_limit: Optional[int] = None
    assume_deterministic: Optional[list[str]] = None


def api_start_picus_v2_task(context: AuditHubContext, input: StartPicusV2TaskArgs):
    logger.debug("Starting Picus V2")

    data = {
        "name": input.name,
        "parameters": get_dict_of_fields_except(
            input, {"organization_id", "project_id", "version_id", "name"}
        ),
    }
    logger.debug("Posting data: %s", data)

    response = authentication_retry(
        context,
        POST,
        url=f"{context.base_url}/organizations/{input.organization_id}/projects/{input.project_id}/versions/{input.version_id}/tools/picus-v2",
        json=data,
    )
    ensure_success(response)
    ret = response_json(response)
    return ret
