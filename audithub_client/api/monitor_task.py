import logging
from dataclasses import dataclass
from json import dumps, loads
from typing import Literal

from websockets import ConnectionClosedOK
from websockets.sync.client import connect

from ..library.auth import get_access_token, get_token_header
from ..library.context import AuditHubContext

logger = logging.getLogger(__name__)

ALLOWED_STATUS_OPTIONS = Literal[
    "Queued",
    "Running",
    "Finished",
    "Failed",
    "Error",
    "Canceled",
    "Pending",
    "Succeeded",
    "Skipped",
]


@dataclass
class MonitorTaskArgs:
    organization_id: int
    task_id: int


def api_monitor_task(context: AuditHubContext, input: MonitorTaskArgs) -> bool:
    access_token = get_access_token(context)
    header = get_token_header(access_token)
    token = header["Authorization"][7:]
    url = context.base_url.replace("http", "ws")
    endpoint = (
        f"{url}/organizations/{input.organization_id}/tasks/{input.task_id}/progress"
    )
    status: ALLOWED_STATUS_OPTIONS
    with connect(endpoint, max_size=100 * 1024 * 1024) as websocket:
        try:
            # send initial authentication
            websocket.send(token)
            while True:
                raw_message = websocket.recv()
                logger.debug("Received: %s", raw_message)
                decoded_message = loads(raw_message)
                kind = decoded_message["kind"]
                task_message = decoded_message["data"]
                if kind == "TaskInfo":
                    status = task_message["status"]
                    if task_message["finished_at"]:
                        logger.info("Task finished with status: %s", status)
                        if status == "Succeeded":
                            return True
                        return False
                    if status == "Running":
                        logger.info("Task started")
                    elif status in {"Pending", "Queued"}:
                        logger.info("Task is pending")
                    elif status in {"Failed", "Error", "Finished", "Canceled"}:
                        logger.info("Task has failed")
                        return False

                elif kind == "TaskStatus":
                    # This arrives as the task makes progress
                    status = task_message["status"]
                    if status == "Succeeded":
                        logger.info("Task finished successfully")
                        return True
                    elif status in {"Failed", "Error", "Finished", "Canceled"}:
                        logger.info("Task finished with status: %s", status)
                        return False
                    else:
                        logger.info("New task status: %s", status)

                elif kind == "TaskStepStarted":
                    step_code = task_message["step_code"]
                    logger.info("Task step %s started", step_code)
                    message = {
                        "kind": "BeginStepLogStream",
                        "data": {
                            "task_id": input.task_id,
                            "step_code": step_code,
                        },
                    }
                    logger.debug("Sending: %s", message)
                    websocket.send(dumps(message))
                elif kind == "TaskStepFinished":

                    logger.info(
                        "Task step %s finished with status %s exit_code %d%s",
                        task_message["step_code"],
                        task_message["status"],
                        task_message["exit_code"],
                        (
                            f" and error: {task_message["error_message"]}"
                            if "error_message" in task_message
                            else ""
                        ),
                    )
                elif kind == "TaskStepLogMessage":
                    print(f"[{task_message["step_code"]}] {task_message["entry"]}")
        except ConnectionClosedOK as ex:
            logger.info("Websocket client: All server logs are received.", ex.reason)
        except Exception as ex:  # pylint: disable=broad-exception-caught
            logger.exception(ex)
    return False
