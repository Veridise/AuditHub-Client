import logging
import sys
from typing import Annotated, Literal, Optional

from cyclopts import Parameter

from ..api.get_configuration import api_get_configuration
from ..api.monitor_task import MonitorTaskArgs, api_monitor_task
from ..api.start_vanguard_task import (
    CustomDetectorFromOrganizationLibrary,
    CustomDetectorFromStandardLibrary,
    CustomDetectorFromVersion,
    CustomDetectorsForTask,
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
        negative_iterable=(),
        help="One or more detector(s) to use for analyzing the sources. For a list of valid detector names, please run `ah get-configuration vanguard_defi_detectors`.",
    ),
]


DefiV2DetectorType = Annotated[
    list[str],
    Parameter(
        consume_multiple=True,
        negative_iterable=(),
        help="One or more detector(s) to use for analyzing the sources. For a list of valid detector names, please run `ah get-configuration vanguard_v2_defi_detectors`.",
    ),
]

DefiV2CustomDetectorFromVersionType = Annotated[
    list[str],
    Parameter(
        consume_multiple=True,
        negative_iterable=(),
        help="An optional list of custom detectors embedded in the version archive.",
    ),
]


def decode_std_lib_custom_detector_from_string(e: str):
    elements = e.strip().split("/")
    if len(elements) != 2:
        raise ValueError(f"Invalid std lib custom detector specification: '{e}'")
    category = elements[0].strip()
    name = elements[1].strip()
    if not category or not name:
        raise ValueError(f"Invalid std lib custom detector specification: '{e}'")
    return CustomDetectorFromStandardLibrary(category=category, name=name)


def validate_std_lib_custom_detector(_t, v):
    for e in v:
        decode_std_lib_custom_detector_from_string(e)
    return True


DefiV2CustomDetectorFromStandardLibraryType = Annotated[
    list[str],
    Parameter(
        validator=validate_std_lib_custom_detector,
        consume_multiple=True,
        negative_iterable=(),
        help="An optional list of custom detectors from the Veridise-maintained standard library. "
        "Use the {category}/{name} notation to specify each entry, i.e., separate these two elements with a forward slash",
    ),
]

DefiV2CustomDetectorFromOrganizationLibraryType = Annotated[
    list[int],
    Parameter(
        consume_multiple=True,
        negative_iterable=(),
        help="An optional list of custom detectors from the organization-level library. Please specify the id of each.",
    ),
]


ZKDetectorType = Annotated[
    list[str],
    Parameter(
        validator=lambda _t, v: len(v) > 0,
        consume_multiple=True,
        negative_iterable=(),
        help="One or more detector(s) to use for analyzing the sources. For a list of valid detector names, please run `ah get-configuration vanguard_zk_detectors`.",
    ),
]

DefiInputLimitType = Annotated[
    Optional[list[str]],
    Parameter(
        negative_iterable=(),
        help="An optional list of source files or directories. If not specified, Vanguard will process all Solidity sources inside the source path specified at the project definition.",
    ),
]

ZKInputLimitType = Annotated[
    str,
    Parameter(
        negative_iterable=(),
        help="A circom source file to process.",
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
    custom_detectors: Optional[CustomDetectorsForTask] = None,
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
            custom_detectors=custom_detectors,
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
    detector: DefiV2DetectorType = list(),
    embedded_custom_detectors: DefiV2CustomDetectorFromVersionType = list(),
    std_lib_custom_detectors: DefiV2CustomDetectorFromStandardLibraryType = list(),
    org_lib_custom_detectors: DefiV2CustomDetectorFromOrganizationLibraryType = list(),
    input_limit: DefiInputLimitType = None,
    wait: TaskWaitType = False,
    rpc_context: AuditHubContextType,
):
    """
    Start a DeFi Vanguard V2 (static analysis) task for a specific version of a project. Outputs the task id.

    """
    custom_detectors: CustomDetectorsForTask = []
    for relative_path in embedded_custom_detectors:
        custom_detectors.append(CustomDetectorFromVersion(relative_path=relative_path))
    for encoded_custom_detector in std_lib_custom_detectors:
        custom_detectors.append(
            decode_std_lib_custom_detector_from_string(encoded_custom_detector)
        )
    for custom_detector_id in org_lib_custom_detectors:
        custom_detectors.append(
            CustomDetectorFromOrganizationLibrary(id=custom_detector_id)
        )

    start_vanguard_common(
        organization_id=organization_id,
        project_id=project_id,
        version_id=version_id,
        name=name,
        detector=detector,
        custom_detectors=custom_detectors,
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
