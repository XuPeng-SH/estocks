import logging
from flask import g
from flask_restplus import marshal, Resource
from restplus_enhancement.schema_model import SchemaResponse
from estocks.namespaces import search_api as api
from estocks.request_parser import search_parser, pagination_parser

logger = logging.getLogger(__name__)


@api.route('/search/stock_exchanges')
class StockExchangesViewSet(Resource):
    @api.expect(search_parser(), validate=True)
    def get(self):
        return 'hello'
