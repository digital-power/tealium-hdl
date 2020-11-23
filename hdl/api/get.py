import json
import requests
from requests.exceptions import RequestException

import hdl.config as cfg

def get_datalayer(datalayer_id):
    """Get Live version of a hosted datalayer file"""
    try:
        response = requests.get(f'{cfg.DLE_URL}{datalayer_id}.js')
        response.raise_for_status()

        datalayer_string = response.text.split(' = ')[-1]

        return json.loads(datalayer_string)

    except RequestException as err:
        print(f'Error occured while getting datalayer "{datalayer_id}": \n {err}')
        return {}
