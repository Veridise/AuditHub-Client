#!/usr/bin/env python3
import logging
from dataclasses import asdict, dataclass
from typing import Literal, Optional

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import POST
from ..library.net_utils import ensure_success, response_json

logger = logging.getLogger(__name__)


@dataclass
class FuzzingBlacklistEntry:
    contract: str
    function: str


@dataclass
class VSpecFromVersion:
    relative_path: str
    type: Literal["version"] = "version"


@dataclass
class VSpecFromStandardLibrary:
    category: str
    name: str
    library_version: Optional[str] = None
    type: Literal["stdlib"] = "stdlib"


@dataclass
class VSpecFromOrganizationLibrary:
    id: int
    type: Literal["orglib"] = "orglib"


@dataclass
class VSpecAdHoc:
    filename: str
    contents: str
    encoding: Literal["plain"] = "plain"
    type: Literal["adhoc"] = "adhoc"


VSpec = (
    VSpecFromVersion
    | VSpecFromStandardLibrary
    | VSpecFromOrganizationLibrary
    | VSpecAdHoc
)


@dataclass
class HintFromVersion:
    relative_path: str
    type: Literal["version"] = "version"


@dataclass
class HintFromStandardLibrary:
    category: str
    name: str
    library_version: Optional[str] = None
    type: Literal["stdlib"] = "stdlib"


@dataclass
class HintFromOrganizationLibrary:
    id: int
    type: Literal["orglib"] = "orglib"


@dataclass
class HintAdHoc:
    filename: str
    contents: str
    encoding: Literal["plain"] = "plain"
    type: Literal["adhoc"] = "adhoc"


Hint = (
    HintFromVersion | HintFromStandardLibrary | HintFromOrganizationLibrary | HintAdHoc
)

ORCA_DEFAULT_TIMEOUT = 600


@dataclass
class OrCaParameters:
    timeout: Optional[int] = None
    disable_user_proxies: Optional[bool] = None
    fuzz_pure: Optional[bool] = None
    fuzz_targets: Optional[list[str]] = None
    fuzzing_blacklist: Optional[list[FuzzingBlacklistEntry]] = None
    fork_network: Optional[str] = None
    fork_block_number: Optional[int] = None
    language: Literal["solidity"] = "solidity"

    def __post_init__(self):
        if self.timeout is None:
            self.timeout = ORCA_DEFAULT_TIMEOUT


@dataclass
class StartOrCaTaskArgs:
    organization_id: int
    project_id: int
    version_id: int
    name: Optional[str]
    parameters: OrCaParameters
    specs: list[VSpec]
    hints: Optional[list[Hint]]
    deployment_script_path_override: Optional[str]


def api_start_orca_task(
    context: AuditHubContext,
    input: StartOrCaTaskArgs,
):
    logger.debug("Starting OrCa")

    data = {
        "name": input.name,
        "parameters": asdict(input.parameters),
        "specs_override": list([asdict(spec) for spec in input.specs]),
        "hints_override": (
            list([asdict(hint) for hint in input.hints]) if input.hints else None
        ),
        "deployment_script_path_override": input.deployment_script_path_override,
    }
    logger.debug("Posting data: %s", data)

    response = authentication_retry(
        context,
        POST,
        url=f"{context.base_url}/organizations/{input.organization_id}/projects/{input.project_id}/versions/{input.version_id}/tools/orca",
        json=data,
    )
    ensure_success(response)
    ret = response_json(response)
    return ret
