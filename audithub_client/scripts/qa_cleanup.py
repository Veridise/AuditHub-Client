import logging

from audithub_client.api.qa_cleanup import api_qa_cleanup

from ..library.invocation_common import AuditHubContextType, app
from ..library.json_dump import OutputType, dump_dict

logger = logging.getLogger(__name__)


@app.command
def qa_cleanup(
    *,
    rpc_context: AuditHubContextType,
    output: OutputType = "json",
):
    """
    Cleanup Q/A generated data.
    """
    try:
        logger.info("Starting...")
        dump_dict(api_qa_cleanup(rpc_context), None, output)
        logger.info("Finished.")
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
