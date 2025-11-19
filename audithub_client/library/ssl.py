from ssl import CERT_NONE, create_default_context

EXCLUDED = ["https://audithub.local.veridise.tools"]


def get_verify_ssl(url: str):
    global EXCLUDED
    for excluded in EXCLUDED:
        if url.startswith(excluded):
            return False
    return True


def get_websocket_ssl_context(url: str) -> dict:
    if url.startswith("ws:"):
        return {}

    verify = True
    global EXCLUDED
    for excluded in EXCLUDED:
        if url.startswith(excluded.replace("http", "ws")):
            verify = False
    if verify:
        return {}
    ctx = create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = CERT_NONE
    return {"ssl": ctx}
