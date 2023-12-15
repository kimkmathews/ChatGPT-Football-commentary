# Extracted from code provided by Supervisor

# Root directory
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_LOCAL_FOLDER = 'D://'

# Signality
os.environ["SIGNALITY_USERNAME"] = ''
os.environ["SIGNALITY_PASSWORD"] = ''
SIGNALITY_USERNAME = os.environ.get('SIGNALITY_USERNAME')
SIGNALITY_PASSWORD = os.environ.get('SIGNALITY_PASSWORD')
os.environ["SIGNALITY_API"] = 'https://api.signality.com'
SIGNALITY_API = os.environ.get('SIGNALITY_API')


WYSCOUT_USER = ''
WYSCOUT_PASS = ''