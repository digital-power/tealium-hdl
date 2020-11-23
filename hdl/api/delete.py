import requests
from requests.exceptions import RequestException

import hdl.config as cfg

from hdl.utility import create_backup
from hdl.api import get_datalayer


def delete_datalayers(datalayer_ids: list) -> None:
    """Delete one or muliple datalayers from the Tealium HDL"""
    for datalayer_id in datalayer_ids:
        old_data = get_datalayer(datalayer_id)

        try:
            response = requests.delete(
                url=cfg.get_api_url() + datalayer_id,
                headers=cfg.REQUEST_HEADERS
            )

            response.raise_for_status()

            status = response.text
            if status == '':
                print(f'Datalayer "{datalayer_id}" succesfully deleted')
                create_backup(
                    action_type=cfg.ACTION_DELETE,
                    datalayer_id=datalayer_id,
                    old=old_data
                )
            else:
                print(f'Unexpected response while deleting datalayer "{datalayer_id}": \n {status}"')

        except RequestException as err:
            print(f'An Error occured during the delete request for "{datalayer_id}": \n {err}')
