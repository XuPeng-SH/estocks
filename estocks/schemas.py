import logging
from flask_restplus import fields
from estocks.namespaces import search_api
from estocks.models import (StockExchangeMetaInfo, StockMetaInfo)

logger = logging.getLogger(__name__)


EmptySchema = search_api.new_schema(name='EmptySchema', fields={
})

StockExchangeMetaInfoSchema = search_api.new_schema(name='StockExchangeMetaInfoSchema', fields={
    'id' : fields.Integer(description='id', readonly=True),
    'display' : fields.String(description='name of exchange', example='上海交易所'),
    'short' : fields.String(description='short name of exchange', example='SH'),
    'code' : fields.String(description='exchange symbol', example='SSH'),
    'country' : fields.String(description='exchange country', example='中国'),
    'extra' : fields.Raw(description='exchange extra info', default={})
})

StockExchangeMetaInfoListSchema = search_api.new_schema(name='StockExchangeMetaInfoListSchema', fields={
    'list': fields.List(fields.Nested(StockExchangeMetaInfoSchema))
})

StockMetaInfoSchema = search_api.new_schema(name='StockMetaInfoSchema', fields={
    'id' : fields.Integer(description='id', readonly=True),
    'display' : fields.String(description='name of stock', example='上海沪工'),
    'symbol' : fields.String(description='stock symbol', example='600131'),
    'industry' : fields.String(description='industry', example='军工'),
    'fullname' : fields.String(description='stock fullname', example='上海沪工有限公司'),
    'enname' : fields.String(description='stock English name', example='SHHG'),
    'market' : fields.String(description='market type name', example='创业板'),
    'extra' : fields.Raw(description='exchange extra info', default={})
})

StockMetaInfoListSchema = search_api.new_schema(name='StockMetaInfoListSchema', fields={
    'list': fields.List(fields.Nested(StockMetaInfoSchema))
})
