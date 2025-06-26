import logging
import sys
from typing import Annotated, Literal, Optional

from cyclopts import Parameter

from ..api.get_configuration import api_get_configuration
from ..api.monitor_task import MonitorTaskArgs, api_monitor_task
from ..api.start_vanguard_task import (
    StartVanguardTaskArgs,
    api_start_vanguard_task,
)
from ..library.invocation_common import (
    AuditHubContextType,
    OrganizationIdType,
    ProjectIdType,
    TaskNameType,
    TaskWaitType,
    VersionIdType,
    app,
)

logger = logging.getLogger(__name__)


DefiDetectorType = Annotated[
    list[str],
    Parameter(
        validator=lambda _t, v: len(v) > 0,
        consume_multiple=True,
        help="One or more detector(s) to use for analyzing the sources. For a list of valid detector names, please run `ah get-configuration vanguard_defi_detectors`.",
    ),
]


DefiV2DetectorType = Annotated[
    list[str],
    Parameter(
        validator=lambda _t, v: len(v) > 0,
        consume_multiple=True,
        help="One or more detector(s) to use for analyzing the sources. For a list of valid detector names, please run `ah get-configuration vanguard_v2_defi_detectors`.",
    ),
]


ZKDetectorType = Annotated[
    list[str],
    Parameter(
        validator=lambda _t, v: len(v) > 0,
        consume_multiple=True,
        help="One or more detector(s) to use for analyzing the sources. For a list of valid detector names, please run `ah get-configuration vanguard_zk_detectors`.",
    ),
]

DefiInputLimitType = Annotated[
    Optional[list[str]],
    Parameter(
        help="An optional list of source files or directories. If not specified, Vanguard will process all Solidity sources inside the source path specified at the project definition.",
    ),
]

ZKInputLimitType = Annotated[
    str,
    Parameter(
        help="A circom source files to process.",
    ),
]

supported_detectors_keys = {
    "vanguard": "vanguard_defi_detectors",
    "vanguard-v2": "vanguard_v2_defi_detectors",
    "zk-vanguard": "vanguard_zk_detectors",
}


def start_vanguard_common(
    *,
    organization_id: OrganizationIdType,
    project_id: ProjectIdType,
    version_id: VersionIdType,
    name: TaskNameType,
    detector: list[str],
    input_limit: Optional[list[str]],
    wait: bool = False,
    rpc_context: AuditHubContextType,
    tool_name: Literal["vanguard", "vanguard-v2", "zk-vanguard"],
):
    try:
        configuration = api_get_configuration(rpc_context)

        supported_detectors = set(
            [e["code"] for e in configuration[supported_detectors_keys[tool_name]]]
        )
        for d in detector:
            if d not in supported_detectors:
                raise ValueError(f"'{d}' is not a valid detector name.")

        rpc_input = StartVanguardTaskArgs(
            organization_id=organization_id,
            project_id=project_id,
            version_id=version_id,
            name=name,
            detector=detector,
            input_limit=input_limit,
            tool_name=tool_name,
        )
        logger.debug("Starting...")
        logger.debug(str(rpc_input))
        ret = api_start_vanguard_task(rpc_context, rpc_input)
        logger.debug("Response: %s", ret)
        task_id = ret["task_id"]
        print(task_id)
        if wait:
            result = api_monitor_task(
                rpc_context,
                MonitorTaskArgs(
                    organization_id=rpc_input.organization_id, task_id=task_id
                ),
            )
        logger.debug("Finished.")
        if wait and not result:
            sys.exit(1)
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)


@app.command
def start_defi_vanguard_task(
    *,
    organization_id: OrganizationIdType,
    project_id: ProjectIdType,
    version_id: VersionIdType,
    name: TaskNameType = None,
    detector: DefiDetectorType,
    input_limit: DefiInputLimitType = None,
    wait: TaskWaitType = False,
    rpc_context: AuditHubContextType,
):
    """
    Start a DeFi Vanguard (static analysis) task for a specific version of a project. Outputs the task id.

    """
    start_vanguard_common(
        organization_id=organization_id,
        project_id=project_id,
        version_id=version_id,
        name=name,
        detector=detector,
        input_limit=input_limit,
        wait=wait,
        rpc_context=rpc_context,
        tool_name="vanguard",
    )


@app.command
def start_defi_vanguard_v2_task(
    *,
    organization_id: OrganizationIdType,
    project_id: ProjectIdType,
    version_id: VersionIdType,
    name: TaskNameType = None,
    detector: DefiV2DetectorType,
    input_limit: DefiInputLimitType = None,
    wait: TaskWaitType = False,
    rpc_context: AuditHubContextType,
):
    """
    Start a DeFi Vanguard V2 (static analysis) task for a specific version of a project. Outputs the task id.

    """
    start_vanguard_common(
        organization_id=organization_id,
        project_id=project_id,
        version_id=version_id,
        name=name,
        detector=detector,
        input_limit=input_limit,
        wait=wait,
        rpc_context=rpc_context,
        tool_name="vanguard-v2",
    )


@app.command
def start_zk_vanguard_task(
    *,
    organization_id: OrganizationIdType,
    project_id: ProjectIdType,
    version_id: VersionIdType,
    name: TaskNameType = None,
    detector: ZKDetectorType,
    input_limit: ZKInputLimitType,
    wait: TaskWaitType = False,
    rpc_context: AuditHubContextType,
):
    """
    Start a ZK Vanguard (static analysis) task for a specific version of a project. Outputs the task id.

    """
    start_vanguard_common(
        organization_id=organization_id,
        project_id=project_id,
        version_id=version_id,
        name=name,
        detector=detector,
        input_limit=[input_limit],
        wait=wait,
        rpc_context=rpc_context,
        tool_name="zk-vanguard",
    )
