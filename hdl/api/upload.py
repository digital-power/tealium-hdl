import json
import requests
from requests.exceptions import RequestException

import hdl.config as cfg


def upload_datalayer(datalayer_id, data):
    """Upload a file trough the tealium HDL API"""
    try:
        request_url = cfg.get_api_url() + datalayer_id

        response = requests.post(
            url=request_url,
            data=json.dumps(data),
            headers=cfg.REQUEST_HEADERS
        )

        status = response.text
        if status == '':
            status = 'success'

        print(
            f'The file: "{datalayer_id}" uploaded as a datalayer to Tealium HDL with status: "{status}"')

        return True

    except RequestException as err:
        print(f'> An error occurred during the API request to Tealium: \n {err}')

    return False
