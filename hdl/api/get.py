import json
from json import JSONDecodeError
import requests
from requests.exceptions import RequestException

import hdl.config as cfg

def get_datalayer(datalayer_id):
    """Get Live version of a hosted datalayer file."""
    try:
        dle_url = f'{cfg.get_dle_url()}{datalayer_id}.js'
        response = requests.get(dle_url)
        response.raise_for_status()

        datalayer_string = response.text.split(' = ')[-1]

        return json.loads(datalayer_string)

    except RequestException as err:
        print(f'Error occured while getting datalayer "{datalayer_id}": \n {err}')
        return {}

    except JSONDecodeError as err:
        print(f'Error occured while parsing datalayer "{datalayer_id}": \n {err}')
