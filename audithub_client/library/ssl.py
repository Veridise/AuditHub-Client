EXCLUDED = ["https://audithub.local.veridise.tools"]


def get_dynamic_verify_ssl(url: str):
    global EXCLUDED
    for excluded in EXCLUDED:
        if url.startswith(excluded):
            return False
    return True
