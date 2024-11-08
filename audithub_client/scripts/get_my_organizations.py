import logging

from ..api.get_my_organizations import api_get_my_organizations
from ..library.invocation_common import AuditHubContextType, app
from ..library.json_dump import OutputType, dump_dict

logger = logging.getLogger(__name__)


@app.command
def get_my_organizations(
    *,
    rpc_context: AuditHubContextType,
    output: OutputType = "json",
):
    """
    Get the organizations the user has been granted access to.
    """
    try:
        logger.debug("Starting...")
        dump_dict(api_get_my_organizations(rpc_context), None, output)
        logger.debug("Finished.")
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
