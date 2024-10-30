from json import JSONDecodeError

from requests import Response

from .utils import parent_func


def ensure_success(response: Response):
    try:
        response.raise_for_status()
    except Exception as ex:
        raise RuntimeError(
            f"Unexpected exit status {response.status_code} at {parent_func()} body={response.text}"
        ) from ex


def response_json(response: Response):
    try:
        return response.json()
    except JSONDecodeError:
        raise RuntimeError(
            f"Could not decode response at {parent_func()}, body: {response.text}"
        ) from None
