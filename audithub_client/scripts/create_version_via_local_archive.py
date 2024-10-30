import logging

from cyclopts.types import ExistingFile

from ..api.create_version_via_local_archive import (
    CreateVersionViaLocalArchiveArgs,
    api_create_version_via_local_archive,
)
from ..library.invocation_common import (
    AuditHubContextType,
    OrganizationIdType,
    ProjectIdType,
    app,
)

logger = logging.getLogger()


@app.command
def create_version_via_local_archive(
    *,
    organization_id: OrganizationIdType,
    project_id: ProjectIdType,
    name: str,
    archive_path: ExistingFile,
    rpc_context: AuditHubContextType,
):
    """
    Create a new version for a project by uploading a local .zip archive.

    Parameters
    ----------
    name:
        The name of the new version to be created
    archive_path:
        The local path to the version .zip archive. Must exist.
    """
    try:
        rpc_input = CreateVersionViaLocalArchiveArgs(
            organization_id=organization_id,
            project_id=project_id,
            name=name,
            archive_path=archive_path,
        )
        logger.debug("Starting...")

        file_size = archive_path.stat().st_size

        logger.info(
            "Posting version archive %s of size %d bytes", archive_path, file_size
        )

        ret = api_create_version_via_local_archive(rpc_context, rpc_input)
        logger.debug("New version response %d", ret)
        print(ret["id"])
        logger.debug("Finished.")
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
