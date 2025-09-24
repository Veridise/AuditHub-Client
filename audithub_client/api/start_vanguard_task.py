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
class CustomDetectorFromVersion:
    relative_path: str
    type: Literal["version"] = "version"


@dataclass
class CustomDetectorFromStandardLibrary:
    category: str
    name: str
    library_version: Optional[str] = None
    type: Literal["stdlib"] = "stdlib"


@dataclass
class CustomDetectorFromOrganizationLibrary:
    id: int
    type: Literal["orglib"] = "orglib"


CustomDetectorsForTask = list[
    CustomDetectorFromVersion
    | CustomDetectorFromStandardLibrary
    | CustomDetectorFromOrganizationLibrary
]


class NoDetectorsDefinedError(ValueError):
    def __init__(self):
        super().__init__("No detectors defined, standard or custom!")


@dataclass
class StartVanguardTaskArgs:
    organization_id: int
    project_id: int
    version_id: int
    name: Optional[str]
    detector: list[str]
    custom_detectors: Optional[CustomDetectorsForTask]

    input_limit: Optional[list[str]]
    tool_name: Literal["vanguard", "vanguard-v2", "zk-vanguard"]


def api_start_vanguard_task(context: AuditHubContext, input: StartVanguardTaskArgs):
    logger.debug("Starting Vanguard")
    count_custom_detectors = (
        0 if input.custom_detectors is None else len(input.custom_detectors)
    )
    count_detectors = len(input.detector)
    if count_custom_detectors + count_detectors == 0:
        raise NoDetectorsDefinedError()

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
