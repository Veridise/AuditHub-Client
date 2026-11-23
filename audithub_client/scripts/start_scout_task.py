import logging
import sys
from typing import Annotated, Optional

from cyclopts import Parameter

from ..api.monitor_task import MonitorTaskArgs, api_monitor_task
from ..api.start_scout_task import (
    ScoutParameters,
    StartScoutTaskArgs,
    api_start_scout_task,
)
from ..library.invocation_common import (
    AuditHubContextType,
    BooleanArg,
    OrganizationIdType,
    ProjectIdType,
    TaskNameType,
    TaskWaitType,
    VersionIdType,
    app,
)

logger = logging.getLogger(__name__)


@app.command
def start_scout_task(
    *,
    organization_id: OrganizationIdType,
    project_id: ProjectIdType,
    version_id: VersionIdType,
    budget: str,
    name: TaskNameType = None,
    input_limit: Annotated[
        Optional[list[str]], Parameter(consume_multiple=True, negative_iterable=())
    ] = None,
    extra_context: Optional[str] = None,
    generate_pocs: BooleanArg = False,
    wait: TaskWaitType = False,
    rpc_context: AuditHubContextType,
):
    """
    Start a Scout scan for a specific version of a project. Outputs the task id.

    Parameters
    ----------
    budget:
        The name of the budget class to use.

    input_limit:
        Source files to process, with paths relative to the version root.
        Files must be inside the project's src_path. If omitted, all files in src_path are processed.

    extra_context:
        Extra context for the scan, supplied as Markdown text.

    generate_pocs
    """
    try:
        rpc_input = StartScoutTaskArgs(
            organization_id=organization_id,
            project_id=project_id,
            version_id=version_id,
            budget=budget,
            name=name,
            parameters=ScoutParameters(
                input_limit=input_limit,
                extra_context=extra_context,
                generate_pocs=generate_pocs,
            ),
        )
        ret = api_start_scout_task(rpc_context, rpc_input)
        task_id = ret["task_id"]
        print(task_id)
        if wait and not api_monitor_task(
            rpc_context,
            MonitorTaskArgs(organization_id=organization_id, task_id=task_id),
        ):
            sys.exit(1)
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
        sys.exit(1)
