ACCOUNT = ''
PROFILE = ''

REQUEST_HEADERS = {
    'Authorization': '',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

AUTH_URL = 'https://api.tealiumiq.com/v2/auth'

def get_dle_url():
    """Return Live HDL URL"""
    return f'https://tags.tiqcdn.com/dle/{ACCOUNT}/{PROFILE}/'

def get_api_url():
    """Return Tealium API Base URL"""
    return f'https://api.tealiumiq.com/v2/dle/accounts/{ACCOUNT}/profiles/{PROFILE}/datalayers/'

OPEN_MENU = ''

ACTION_CREATE = 'CREATE'
ACTION_UPDATE = 'UPDATE'
ACTION_DELETE = 'DELETE'

BACKUP_FOLDER = 'backups'
