import requests
from requests.exceptions import RequestException

import hdl.config as cfg

def auth(username, key) -> bool:
    """Get API token from the Tealium Auth service"""
    tealium_token = ''
    try:
        response = requests.post(
            cfg.AUTH_URL,
            data={
                'username': username,
                'key': key
            }
        )

        response.raise_for_status()

        tealium_token = response.json()['token']

        cfg.REQUEST_HEADERS['Authorization'] = f'Bearer {tealium_token}'

        return True

    except RequestException:
        print('Error: Wrong Tealium credentials or API key.')
        return False
