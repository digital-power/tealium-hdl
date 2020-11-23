ACCOUNT = ''
PROFILE = ''

REQUEST_HEADERS = {
    'Authorization': '',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

AUTH_URL = 'https://api.tealiumiq.com/v2/auth'
DLE_URL = 'https://tags.tiqcdn.com/dle/unive/adv-unive-nl/'

def get_api_url():
    """Return Tealium API Base URL"""
    return f'https://api.tealiumiq.com/v2/dle/accounts/{ACCOUNT}/profiles/{PROFILE}/datalayers/'

OPEN_MENU = ''

ACTION_CREATE = 'CREATE'
ACTION_UPDATE = 'UPDATE'
ACTION_DELETE = 'DELETE'

BACKUP_FOLDER = 'backups'
