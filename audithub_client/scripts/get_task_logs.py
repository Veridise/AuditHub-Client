import logging

from ..api.get_task_logs import GetTaskLogsArgs, api_get_task_logs
from ..library.invocation_common import (
    AuditHubContextType,
    OrganizationIdType,
    TaskIdType,
    app,
)
from ..library.json_dump import OutputType, dump_dict

logger = logging.getLogger(__name__)


@app.command
def get_task_logs(
    *,
    organization_id: OrganizationIdType,
    task_id: TaskIdType,
    step_code: str,
    output: OutputType = "list",
    rpc_context: AuditHubContextType,
):
    """
    Get logs of a task's step.

    Parameters
    ----------
    task_id:
        The id of the task.
    step_code:
        The step_code. You can use `ah get-task-info` to obtain the list of valid steps.
    output:
        The output style. Text writes each log entry in a log, json returns log entries as a JSON array.
    """
    try:
        rpc_input = GetTaskLogsArgs(
            organization_id=organization_id, task_id=task_id, step_code=step_code
        )
        logger.debug("Starting...")
        logger.debug(str(input))
        ret = api_get_task_logs(rpc_context, rpc_input)

        dump_dict(ret, None, output)
        logger.debug("Finished.")
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
