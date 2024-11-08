import logging
from typing import Optional

from ..api.get_my_profile import api_get_my_profile
from ..library.invocation_common import AuditHubContextType, app
from ..library.json_dump import OutputType, dump_dict

logger = logging.getLogger(__name__)


@app.command
def get_my_profile(
    section: Optional[str] = None,
    *,
    rpc_context: AuditHubContextType,
    output: OutputType = "json",
):
    """
    Get the profile of the user.

    Parameters
    ----------
    section:
        The profile section to list. Use 'sections' to list all valid sections.  If empty, outputs the complete JSON document.
    """
    try:
        logger.debug("Starting...")
        dump_dict(api_get_my_profile(rpc_context), section, output)
        logger.debug("Finished.")
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
