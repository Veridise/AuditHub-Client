import logging
import sys

from ..api.monitor_task import MonitorTaskArgs, api_monitor_task
from ..library.invocation_common import (
    AuditHubContextType,
    OrganizationIdType,
    TaskIdType,
    app,
)

logger = logging.getLogger(__name__)


@app.command
def monitor_task(
    task_id: TaskIdType,
    *,
    organization_id: OrganizationIdType,
    rpc_context: AuditHubContextType,
):
    """
    Monitor a task's progress. Will exit with an exit status of 1 if the task did not complete successfully.

    Parameters
    ----------
    task_id:
        The id of the task.
    """
    try:
        rpc_input = MonitorTaskArgs(
            organization_id=organization_id,
            task_id=task_id,
        )
        logger.debug("Starting...")
        logger.debug(str(input))
        ret = api_monitor_task(rpc_context, rpc_input)
        if not ret:
            logger.error("Task failed to complete successfully.")
            sys.exit(1)

        logger.debug("Finished.")
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
