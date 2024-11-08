import logging
from pathlib import Path
from typing import Annotated

from cyclopts import Parameter

from ..api.get_task_artifact import GetTaskArtifactArgs, api_get_artifact
from ..library.invocation_common import AuditHubContextType, OrganizationIdType, app

logger = logging.getLogger(__name__)


@app.command
def get_task_artifact(
    *,
    organization_id: OrganizationIdType,
    task_id: Annotated[int, Parameter(name=["--task-id", "-t"])],
    artifact_id: int,
    output_file: Path,
    rpc_context: AuditHubContextType,
):
    """
    DownGet logs of a task's step.

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
        response = api_get_artifact(rpc_context, rpc_input)
        with output_file.open("wb") as f:
            f.write(response.content)
        logger.debug("Finished.")
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
