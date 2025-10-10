import logging
from pathlib import Path

from ..api.get_task_artifact import GetTaskArtifactArgs, api_get_artifact
from ..library.invocation_common import (
    AuditHubContextType,
    OrganizationIdType,
    TaskIdType,
    app,
)
from ..library.net_utils import Downloader

logger = logging.getLogger(__name__)


@app.command
def get_task_artifact(
    *,
    organization_id: OrganizationIdType,
    task_id: TaskIdType,
    artifact_id: int,
    output_file: Path,
    rpc_context: AuditHubContextType,
):
    """
    Download a task's artifact, by its id.

    Parameters
    ----------
    task_id:
        The id of the task.
    artifact_id:
        The id of the artifact. You can use `ah get-task-info` to obtain the list of produced artifacts.
    output_file:
        The local file name to store the output in.
    """
    try:
        rpc_input = GetTaskArtifactArgs(
            organization_id=organization_id, task_id=task_id, artifact_id=artifact_id
        )
        logger.debug("Starting...")
        logger.debug(str(input))
        downloader = Downloader(output_file)
        api_get_artifact(rpc_context, rpc_input, downloader)
        logger.info(f"Wrote {downloader.bytes_written} bytes ({downloader.hr_size}).")
        logger.debug("Finished.")
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
