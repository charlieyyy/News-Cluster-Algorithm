import os

MAIL_SERVICE_API_KEY = os.environ.get('MAIL_SERVICE_API_KEY')
DEFAULT_MAIL_LIST = os.environ.get(
    'DEFUALT_MAIL_LIST',
    'caihaoyu@geekpark.net,chywj7@gmail.com').split(',')
MAIL_SERVICE_HOST = 'http://kong.geeks.vc/api/v1/mail'

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', '27017'))
DB_NAME = os.environ.get('DB_NAME', 'geek_digest')
