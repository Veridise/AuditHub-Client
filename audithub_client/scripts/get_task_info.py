import logging
import sys
from typing import Optional

from ..api.get_task_info import GetTaskInfoArgs, api_get_task_info
from ..library.invocation_common import (
    AuditHubContextType,
    BooleanArg,
    OrganizationIdType,
    TaskIdType,
    app,
)
from ..library.json_dump import OutputType, dump_dict

logger = logging.getLogger(__name__)


@app.command
def get_task_info(
    section: Optional[str] = None,
    *,
    organization_id: OrganizationIdType,
    task_id: TaskIdType,
    output: OutputType = "json",
    verify: BooleanArg = False,
    check_completed: BooleanArg = False,
    rpc_context: AuditHubContextType,
):
    """
    Get detailed task information.

    Parameters
    ----------
    task_id:
        The id of the task.
    section:
        The task information section to output. Use 'sections' to list all valid sections. If empty, outputs the complete JSON document.
    verify:
        If true, the findings counters are summed. If the sum if zero, the exit code is 0, otherwise it is 1.
        i.e., an exit code of 1 means there is at least one finding in one of the findings categories.
        This argument is independent of any output arguments.
    check_completed:
        If true, all steps that are "tools" are checked to see if they reported completed == false.
        In such a case, we produce a 'timeout error' with an exit code of 2
    """
    try:
        rpc_input = GetTaskInfoArgs(organization_id=organization_id, task_id=task_id)
        exit_code = 0
        logger.debug("Starting...")
        logger.debug(str(rpc_input))
        task_info = api_get_task_info(rpc_context, rpc_input)
        dump_dict(task_info, section, output)
        if verify:
            findings_counters = task_info.get("findings_counters")
            if findings_counters is not None:
                keys = list(findings_counters.keys())
                if keys:
                    total = sum([findings_counters[k] for k in keys])
                    if total > 0:
                        print(
                            "A total of",
                            total,
                            "findings were reported by this task, exiting with 1",
                        )
                        exit_code = 1
            if exit_code == 0:
                print("No findings reported by this task, exiting with 0")
        if exit_code == 0 and check_completed:
            for step in task_info.get("steps", list()):
                completed = step.get("completed_without_timeout", None)
                if completed is not None:
                    if not completed:
                        exit_code = 2
                        print(
                            "Step",
                            step.get("code"),
                            "reported that it hit a timeout and could not complete its work",
                        )

        logger.debug("Finished.")
        sys.exit(exit_code)
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
