import os

from dotenv import load_dotenv
from json import loads

load_dotenv()

DEBUG = os.environ['DEBUG'] or True

SELENOID_HOST = os.environ['SELENOID_HOST'] or 'localhost'
SELENOID_PORT = os.environ['SELENOID_PORT'] or 4444

SUPPLIERS_AUTH = loads(os.environ['SUPPLIERS_AUTH'])
# словарь с авторизационными данными каждого поставщика следующего вида:
# {
#     'supplier_name': {
#         'login': 'foo',
#         'password': 'bar'
#     }
# }
