import requests
from requests.exceptions import RequestException

import hdl.config as cfg


def datalayer_exists(datalayer_id):
    """Check if datalayer exists"""
    try:
        response = requests.get(
            url=cfg.get_api_url() + datalayer_id,
            headers=cfg.REQUEST_HEADERS
        )

        response.raise_for_status()

        return True
    except RequestException:
        return False
