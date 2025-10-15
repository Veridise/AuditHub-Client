import logging
import sys
from pathlib import Path
from time import sleep
from typing import Annotated

from cyclopts import Parameter, validators

from ..api.get_task_info import GetTaskInfoArgs, api_get_task_info
from ..library.http_download import download_from_url
from ..library.invocation_common import (
    AuditHubContextType,
    OrganizationIdType,
    TaskIdType,
    app,
)

logger = logging.getLogger(__name__)


@app.command
def download_artifact(
    *,
    organization_id: OrganizationIdType,
    task_id: TaskIdType,
    step_code: str,
    name: str,
    output_file: Path,
    timeout: Annotated[int, Parameter(validator=validators.Number(gt=0))] = 30,
    rpc_context: AuditHubContextType,
):
    """
    Download an artifact by name, potentially waiting for it to become available.

    This is an improved version of get-task-artifact, that potentially waits for the artifact to become
    available and downloads it using the provided URL.

    Note that you can use 'ah get-task-info' to obtain the list of step_codes
    (key 'steps') and produced artifacts (key 'artifacts').

    Also note that, due to the asynchronous nature of AuditHub, artifacts may take a short amount of time
    until they become available, even when the task has finished.
    This is normal, and this command takes this into account.

    Parameters
    ----------
    step_code:
        The code of the workflow step that produced the artifact
    name:
        The name of the artifact.
    output_file:
        The local file name to store the output in.
    timeout:
        The number of seconds to potentially wait for the artifact to become available.
    """
    try:
        found = False
        for attempt in range(1, timeout + 1):
            logger.debug("Starting attempt %d", attempt)
            task_info = api_get_task_info(
                rpc_context,
                GetTaskInfoArgs(organization_id=organization_id, task_id=task_id),
            )
            matched_artifacts = [
                e
                for e in task_info.get("artifacts", list())
                if e.get("step_code") == step_code and e.get("name") == name
            ]
            if len(matched_artifacts) > 1:
                # This should be impossible
                raise RuntimeError(
                    f"Multiple artifacts matched the condition, bailing: '{matched_artifacts}'"
                )
            if len(matched_artifacts) == 1:
                logger.debug("Artifact found at attempt %d, downloading...", attempt)
                bytes_written, hr_size = download_from_url(
                    matched_artifacts[0]["presigned_url"], output_file
                )
                logger.info(
                    f"Downloaded {bytes_written} bytes ({hr_size}) as {output_file}."
                )
                found = True
                break
            else:
                logger.info(
                    "Artifact not found, waiting a sec at attempt %d..", attempt
                )
                sleep(1)

        if found:
            logger.debug("Finished.")
        else:
            logger.error("Artifact not found (yet?).")
            sys.exit(1)

    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
