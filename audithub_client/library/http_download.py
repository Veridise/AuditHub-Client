from pathlib import Path
from typing import Tuple

from httpx import Client

from audithub_client.library.net_utils import download_file

from .auth import DEFAULT_REQUEST_TIMEOUT


def download_from_url(
    url: str, output_file: Path, timeout=DEFAULT_REQUEST_TIMEOUT
) -> Tuple[int, str]:
    """This is a `curl -o`/`wget -O` equivalent"""
    with Client(timeout=timeout) as client:
        with client.stream("GET", url) as response:
            return download_file(response, output_file)
