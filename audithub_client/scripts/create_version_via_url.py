import logging
from typing import Literal, Optional

from ..api.create_version_via_url import (
    CreateVersionViaUrlArgs,
    api_create_version_via_url,
)
from ..library.invocation_common import (
    AuditHubContextType,
    OrganizationIdType,
    ProjectIdType,
    app,
)

logger = logging.getLogger(__name__)


@app.command
def create_version_via_url(
    *,
    organization_id: OrganizationIdType,
    project_id: ProjectIdType,
    name: str,
    input_type: Literal["git", "archive"],
    url: str,
    revision: Optional[str] = None,
    includes_submodules: Optional[bool] = None,
    rpc_context: AuditHubContextType,
):
    """
    Create a new version for a project by uploading a local .zip archive.

    Parameters
    ----------
    name:
        The name of the new version to be created
    input_type:
        The input type, i.e., how to access the specified url.
    url:
        The url to AuditHub should download data from.
    revision:
        An optional revision, such as branch name, commit hash, or tag, in case of git repos.
    includes_submodules:
        In case of git, if the repo contains submodules that AuditHub should also check out during clone.
    """
    try:
        rpc_input = CreateVersionViaUrlArgs(
            organization_id=organization_id,
            project_id=project_id,
            name=name,
            input_type=input_type,
            url=url,
            revision=revision,
            includes_submodules=includes_submodules,
        )
        logger.debug("Starting...")
        logger.debug(str(input))
        ret = api_create_version_via_url(rpc_context, rpc_input)
        logger.debug("New version response %d", ret)
        print(ret["id"])
        logger.debug("Finished.")
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
