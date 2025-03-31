import logging
from pathlib import Path

from ..api.get_version_archive import GetVersionArchiveArgs, api_get_version_archive
from ..library.invocation_common import (
    AuditHubContextType,
    OrganizationIdType,
    ProjectIdType,
    VersionIdType,
    app,
)
from ..library.net_utils import download_file

logger = logging.getLogger(__name__)


@app.command
def get_version_archive(
    *,
    organization_id: OrganizationIdType,
    project_id: ProjectIdType,
    version_id: VersionIdType,
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
        rpc_input = GetVersionArchiveArgs(
            organization_id=organization_id,
            project_id=project_id,
            version_id=version_id,
        )
        logger.debug("Starting...")
        logger.debug(str(input))
        response = api_get_version_archive(rpc_context, rpc_input)
        bytes_written, hr_size = download_file(response, output_file)
        logger.info(f"Wrote {bytes_written} bytes ({hr_size}).")
        logger.debug("Finished.")
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
