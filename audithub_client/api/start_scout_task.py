import logging
from dataclasses import asdict, dataclass
from typing import Optional

from ..library.auth import authentication_retry
from ..library.context import AuditHubContext
from ..library.http import POST
from ..library.net_utils import ensure_success, response_json

logger = logging.getLogger(__name__)


@dataclass
class ScoutParameters:
    input_limit: Optional[list[str]] = None
    extra_context: Optional[str] = None
    generate_pocs: bool = False


@dataclass
class StartScoutTaskArgs:
    organization_id: int
    project_id: int
    version_id: int
    budget: str
    parameters: ScoutParameters
    name: Optional[str] = None


def api_start_scout_task(context: AuditHubContext, input: StartScoutTaskArgs):
    logger.debug("Starting Scout")
    data = {
        "budget": input.budget,
        "parameters": asdict(input.parameters),
    }
    if input.name is not None:
        data["name"] = input.name

    response = authentication_retry(
        context,
        POST,
        url=f"{context.base_url}/organizations/{input.organization_id}/projects/{input.project_id}/versions/{input.version_id}/tools/agent",
        json=data,
    )
    ensure_success(response)
    return response_json(response)
