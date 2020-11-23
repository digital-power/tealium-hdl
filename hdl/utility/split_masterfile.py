import os
import json
from collections.abc import Mapping

from .folders import create_folder, generate_folder_name

def validate_master(data):
    """Validate if all keys contain a dictionary"""
    if isinstance(data, Mapping):
        for _key, value in data.items():
            if isinstance(value, Mapping):
                pass
            else:
                return False
        return True
    return False


def split_masterfile(file_paths_list):
    """Split a masterfile (a collection of multiple datalayer JSONs) into multiple files"""
    for file_path in file_paths_list:
        data = {}
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except ValueError:
                print(f'The file "{file_path}" does not contain a correct JSON format')

        if validate_master(data):
            folder_name = generate_folder_name('_master_split')
            folder_path = os.path.join(os.getcwd(), folder_name)

            create_folder(folder_path)

            for key, value in data.items():
                filename = key + '.json'
                with open(os.path.join(folder_path, filename), 'w') as file:
                    file.write(json.dumps(value, indent=4))

            print(f'Written output from "{file_path}" to folder "{folder_name}"')

        else:
            print(f'The file "{file_path}" does not contain the correct master file format')
