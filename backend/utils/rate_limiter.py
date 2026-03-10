TOTAL_REQUESTS = 0
MAX_REQUESTS = 50


def allow_request():
    global TOTAL_REQUESTS

    if TOTAL_REQUESTS >= MAX_REQUESTS:
        return False

    TOTAL_REQUESTS += 1
    return True