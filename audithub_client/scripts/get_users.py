import logging

from ..api.get_users import api_get_users
from ..library.invocation_common import AuditHubContextType, app
from ..library.json_dump import OutputType, dump_dict

logger = logging.getLogger(__name__)


@app.command
def get_users(
    *,
    rpc_context: AuditHubContextType,
    output: OutputType = "json",
):
    """
    Get all registered users.
    """
    try:
        logger.debug("Starting...")
        dump_dict(api_get_users(rpc_context), None, output)
        logger.debug("Finished.")
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
