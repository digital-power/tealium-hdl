import os
import json
from pathlib import Path
from datetime import datetime

from hdl.config import BACKUP_FOLDER

def create_backup(action_type: str, datalayer_id: str, old: None = None, new: None = None):
    """Store backup of actions that have occurred"""
    folder_name = os.path.join(BACKUP_FOLDER, datalayer_id)

    Path(folder_name).mkdir(parents=True, exist_ok=True)

    file_name = f'{datetime.today().strftime("%Y%m%d_%H%M%S")}_{action_type}.json'

    data = {
        'action': action_type,
        'datalayer_id': datalayer_id,
        'old': old if old is not None else {},
        'new': new if new is not None else {}
    }

    with open(os.path.join(folder_name, file_name), 'w') as file:
        file.write(json.dumps(data, indent=4))
