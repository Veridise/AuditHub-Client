verify_ssl = True


def get_verify_ssl():
    global verify_ssl
    return verify_ssl


def set_verify_ssl(value: bool):
    global verify_ssl
    verify_ssl = value
