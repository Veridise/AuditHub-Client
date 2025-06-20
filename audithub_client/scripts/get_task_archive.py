import logging
from pathlib import Path

from ..api.get_task_archive import GetTaskArchiveArgs, api_get_task_archive
from ..library.invocation_common import (
    AuditHubContextType,
    OrganizationIdType,
    TaskIdType,
    app,
)
from ..library.net_utils import Downloader

logger = logging.getLogger(__name__)


@app.command
def get_task_archive(
    *,
    organization_id: OrganizationIdType,
    task_id: TaskIdType,
    output_file: Path,
    rpc_context: AuditHubContextType,
):
    """
    Download the augmented archive logs of a task's step. This archive contains the original project's version that was used
    to start this task, along with any files produced during task execution.

    Parameters
    ----------
    output_file:
        The local file name to store the output in.
    """
    try:
        rpc_input = GetTaskArchiveArgs(organization_id=organization_id, task_id=task_id)
        logger.debug("Starting...")
        logger.debug(str(input))
        downloader = Downloader(output_file)
        api_get_task_archive(rpc_context, rpc_input, downloader)
        logger.info(f"Wrote {downloader.bytes_written} bytes ({downloader.hr_size}).")
        logger.debug("Finished.")
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
