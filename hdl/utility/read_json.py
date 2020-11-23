import json

def read_json(file_path: str) -> dict:
    """Read JSON file"""
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
            return data
        except ValueError:
            print(f'The file: "{file_path}" does not contain a correct JSON format!')
            raise

        except FileNotFoundError:
            print(f'The file: "{file_path}" does not exists')
            raise
