from json import JSONDecodeError
from pathlib import Path
from typing import Tuple

from humanize import naturalsize

from ..library.http import Response
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


def download_file(response: Response, output_file: Path) -> Tuple[int, str]:
    bytes_written = 0
    with output_file.open("wb") as f:
        for chunk in response.iter_content(chunk_size=None):
            bytes_written += f.write(chunk)
    return bytes_written, naturalsize(bytes_written, binary=True)
