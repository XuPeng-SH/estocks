import logging
from pprint import pprint
from flask import g
from flask_restplus import Resource
from restplus_enhancement.schema_model import SchemaResponse
from elasticsearch_dsl import Search, Text, Q, MultiSearch
from estocks.namespaces import search_api as api
from estocks.request_parser import search_parser, pagination_parser
from estocks import es_manager
from estocks.documents import StockExchangeMetaDoc, INDEX
from estocks.models import StockExchangeMetaInfo

logger = logging.getLogger(__name__)


@api.route('/search/stock_exchanges')
class StockExchangesViewSet(Resource):
    @api.expect(search_parser(), validate=True)
    def get(self):
        keyword = g.args.keyword
        q = Q('multi_match', query=keyword, fields=['display', 'code', 'country', 'area'])
        this_search = Search(using=es_manager.client).query(q)[g.args.start:g.args.end]
        logger.debug(this_search.to_dict())
        resp = this_search.execute()
        # for hit in resp.hits:
        #     print(hit.display, dir(hit))

        return [hit.display for hit in resp.hits]

    def delete(self):
        INDEX.delete()

    def post(self):
        exchanges = StockExchangeMetaInfo.query.all()
        for exchange in exchanges:
            doc = StockExchangeMetaDoc(id=exchange.id,
                    display=exchange.display,
                    code=exchange.code,
                    area=exchange.area,
                    country=exchange.country)
            doc.save()
