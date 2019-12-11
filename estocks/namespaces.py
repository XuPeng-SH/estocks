from estocks import api
from restplus_enhancement.namespace import Namespace

search_api = Namespace('SEARCH', description='Search API', path='/', validate=True)
api.add_namespace(search_api)

from estocks import search
