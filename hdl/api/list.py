import json
import requests
from requests.exceptions import RequestException

import hdl.config as cfg

def list_datalayers() -> list:
    """Returns a list of current datalayers for the given Account & Profile"""
    datalayers = []
    try:
        response = requests.get(
            cfg.get_api_url(),
            headers=cfg.REQUEST_HEADERS
        )
        response.raise_for_status()

        file_statuses = json.loads(response.text)['fileStatuses']

        for file_status in file_statuses:
            datalayers.append(file_status['file'].replace(f'dle/{cfg.ACCOUNT}/{cfg.PROFILE}/', '').replace('.js', ''))

        return datalayers
    except RequestException as err:
        print(f'Error occured while fetching a list of all datalayers: \n {err}')
        return datalayers
