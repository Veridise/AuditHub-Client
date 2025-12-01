from httpx import Request as Request
from httpx import Response as Response
from httpx import Timeout as Timeout
from httpx import delete as delete
from httpx import get as get
from httpx import post as post
from httpx import put as put

GET = "GET"
DELETE = "DELETE"
POST = "POST"
PUT = "PUT"

DEFAULT_CONNECT_TIMEOUT = 30
DEFAULT_READ_TIMEOUT = 90
DEFAULT_WRITE_TIMEOUT = 600
DEFAULT_POOL_TIMEOUT = 10

AUTHENTICATION_TIMEOUT = Timeout(
    connect=DEFAULT_CONNECT_TIMEOUT, read=30, write=30, pool=DEFAULT_POOL_TIMEOUT
)
DEFAULT_REQUEST_TIMEOUT = Timeout(
    connect=DEFAULT_CONNECT_TIMEOUT,
    read=DEFAULT_READ_TIMEOUT,
    write=DEFAULT_WRITE_TIMEOUT,
    pool=DEFAULT_POOL_TIMEOUT,
)
