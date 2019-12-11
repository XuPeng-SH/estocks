from estocks import api
from restplus_enhancement.namespace import Namespace

default_api = Namespace('default', description='default API', path='/', validate=False)
search_api = Namespace('SEARCH', description='Search API', path='/', validate=True)

api.add_namespace(default_api)
api.add_namespace(search_api)

from estocks import search
