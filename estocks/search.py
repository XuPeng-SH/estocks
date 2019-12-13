import logging
import datetime as dt
from flask import g
from flask_restplus import Resource
from restplus_enhancement.schema_model import SchemaResponse
from elasticsearch_dsl import Search, Text, Q, MultiSearch, SF, Range
from estocks.namespaces import search_api as api
from estocks.request_parser import search_parser, pagination_parser
from estocks import es_manager
from estocks.documents import (StockExchangeMetaDoc, META_EXCH_INDEX, META_STK_INDEX,
        StockMetaDoc)
from estocks.models import (StockExchangeMetaInfo, StockMetaInfo)
from estocks.schemas import (EmptySchema, StockExchangeMetaInfoSchema,
        StockExchangeMetaInfoListSchema, StockMetaInfoSchema, StockMetaInfoListSchema)

logger = logging.getLogger(__name__)


@api.route('/search/meta/stocks')
class StockMetaViewSet(Resource):
    @api.response(201, 'Success', EmptySchema)
    @api.response(400, 'Error', EmptySchema, validate=False )
    def post(self):
        stocks = StockMetaInfo.query.all()
        for stock in stocks:
            doc = StockMetaDoc(
                    meta={'id': stock.id},
                    id=stock.id,
                    display=stock.display,
                    symbol=stock.symbol,
                    fullname=stock.fullname,
                    market=stock.market,
                    industry=stock.industry,
                    list_date=stock.list_date,
                    area=stock.area)
            doc.save()

        return SchemaResponse()

    @api.response(204, 'Success', EmptySchema, validate=False)
    def delete(self):
        META_STK_INDEX.delete()

        return SchemaResponse()

    def build_q1(self, keyword):
        if not keyword:
            return Q()
        sq1_1 = Q('match_phrase', fullname=keyword)
        sq1_2 = Q('match_phrase', enname=keyword)
        sq1_3 = Q('match_phrase', area=keyword)
        sq1_4 = Q('match_phrase', industry=keyword)
        ssq1 = Q('match_phrase', symbol=keyword)
        ssq2 = Q('match_phrase', display=keyword)

        q = Q('function_score',
            query=Q(),
            boost=1,
            score_mode='max',
            min_score=2,
            functions=[
                SF({'weight': 5, 'filter': ssq1}),
                SF({'weight': 5, 'filter': ssq2}),
                SF({'weight': 1,'filter': sq1_1}),
                SF({'weight': 1,'filter': sq1_2}),
                SF({'weight': 1,'filter': sq1_3}),
                SF({'weight':3, 'filter': sq1_4}),
        ])
        return q

    def build_before_q(self, this_date):
        if not this_date:
            return Q()

        try:
            this_day = dt.datetime.strptime(this_date, "%Y-%m-%d")
        except ValueError:
            return Q()

        return Q('range', list_date={'gt': this_day})

    @api.expect(search_parser(), validate=True)
    @api.response(200, 'Success', StockMetaInfoListSchema)
    @api.response(400, 'Error', EmptySchema, validate=False)
    def get(self):
        keyword = g.args.keyword

        kq = self.build_q1(keyword)
        bq = self.build_before_q(g.args.before)

        q = Q('bool', must=[kq, bq])

        this_search = Search(using=es_manager.client, index=META_STK_INDEX._name).query(q)[g.args.start:g.args.end]
        print(this_search.to_dict())
        resp = this_search.execute()

        stocks = [StockMetaInfo.query.get(hit.id) for hit in resp.hits]
        print([hit.meta.score for hit in resp.hits])
        print([hit.list_date for hit in resp.hits])
        return SchemaResponse(result={
            'meta': {'total': resp.hits.total.value},
            'list': stocks
        })



@api.route('/search/meta/stock_exchanges')
class StockExchangesViewSet(Resource):
    @api.expect(search_parser(), validate=True)
    @api.response(200, 'Success', StockExchangeMetaInfoListSchema)
    @api.response(400, 'Error', EmptySchema, validate=False)
    def get(self):
        keyword = g.args.keyword
        q = Q('multi_match', query=keyword, fields=['display', 'code', 'country', 'area'])
        this_search = Search(using=es_manager.client).query(q)[g.args.start:g.args.end]
        logger.debug(this_search.to_dict())
        resp = this_search.execute()
        # for hit in resp.hits:
        #     print(hit.display, dir(hit))

        exchanges = [StockExchangeMetaInfo.query.get(hit.id) for hit in resp.hits]
        return SchemaResponse(result={
            'list': exchanges
        })

    @api.response(204, 'Success', EmptySchema, validate=False)
    def delete(self):
        META_EXCH_INDEX.delete()

        return SchemaResponse(result={})

    @api.response(201, 'Success', EmptySchema)
    @api.response(400, 'Error', EmptySchema, validate=False )
    def post(self):
        exchanges = StockExchangeMetaInfo.query.all()
        for exchange in exchanges:
            doc = StockExchangeMetaDoc(
                    meta={'id': exchange.id},
                    id=exchange.id,
                    display=exchange.display,
                    code=exchange.code,
                    area=exchange.area,
                    country=exchange.country)
            doc.save()

        return SchemaResponse()
