import logging
from typing import Optional

from ..api.get_configuration import api_get_configuration
from ..library.invocation_common import AuditHubContextType, app
from ..library.json_dump import OutputType, dump_dict

logger = logging.getLogger(__name__)


@app.command
def get_configuration(
    section: Optional[str] = None,
    *,
    output: OutputType = "json",
    rpc_context: AuditHubContextType,
):
    """
    Get global AuditHub configuration.

    Parameters
    ----------
    section:
        The configuration section to list. Use 'sections' to list all valid sections.  If empty, outputs the complete JSON document.
    """
    try:
        logger.debug(f"Starting with {section=} {output=}...")
        dump_dict(api_get_configuration(rpc_context), section, output)
        logger.debug("Finished.")
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
