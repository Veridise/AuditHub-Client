import logging
import sys
from typing import Literal, Optional

from ..api.monitor_task import MonitorTaskArgs, api_monitor_task
from ..api.start_picus_v2_task import StartPicusV2TaskArgs, api_start_picus_v2_task
from ..library.invocation_common import (
    AuditHubContextType,
    OrganizationIdType,
    ProjectIdType,
    VersionIdType,
    app,
)

logger = logging.getLogger(__name__)


@app.command
def start_picus_v2_task(
    source: str,
    *,
    organization_id: OrganizationIdType,
    project_id: ProjectIdType,
    version_id: VersionIdType,
    name: Optional[str] = None,
    solver: Optional[Literal["cvc5", "cvc5-int", "z3", "multi-solver"]] = None,
    solver_timeout: Optional[int] = None,
    time_limit: Optional[int] = None,
    assume_deterministic: Optional[list[str]] = None,
    wait: bool = False,
    rpc_context: AuditHubContextType,
):
    """
    Start a Picus V2 (Rust version) task for a module of a specific version of a project. Outputs the task id.

    Parameters
    ----------
    name:
        An optional task name for this task. If not specified, one will automatically be generated by AuditHub.

    source:
        The path, relative to the version root, of the .picus file to process.

    solver:
        Specifies the solver to use.
        cvc5 indicates the finite field solver,
        cvc5-int is a fork of the finite field solver which supports mixed reasoning,
        multi-solver indicates using both cvc5 and cvc5-int,
        and z3 is the z3 integer solver.
        Defaults to "vcv5-int" if no value is specified.

    solver_timeout:
        Timeout set for each solver query, in milliseconds (default: 5000 ms).

    time_limit:
        Global timeout. If Picus takes longer than the time_limit provided then it will terminate.
        Value in milliseconds (default: unlimited).

    assume_deterministic:
        An optional list of modules inside the selected source file.
        Tells Picus to assume the list of modules provided are deterministic.

    wait:
        If specified, this script will monitor the task and wait for it to finish. The exit code will reflect the success or failure of the task, regardless of findings produced by the analysis.
    """
    try:
        rpc_input = StartPicusV2TaskArgs(
            organization_id=organization_id,
            project_id=project_id,
            version_id=version_id,
            name=name,
            source=source,
            solver=solver,
            solver_timeout=solver_timeout,
            time_limit=time_limit,
            assume_deterministic=assume_deterministic,
        )
        logger.debug("Starting...")
        logger.debug(str(input))
        ret = api_start_picus_v2_task(rpc_context, rpc_input)
        logger.debug("Response: %s", ret)
        task_id = ret["task_id"]
        print(task_id)
        if wait:
            result = api_monitor_task(
                rpc_context,
                MonitorTaskArgs(organization_id=organization_id, task_id=task_id),
            )
        logger.debug("Finished.")
        if wait and not result:
            sys.exit(1)
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
