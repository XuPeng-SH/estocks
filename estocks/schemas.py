import logging
from flask_restplus import fields
from estocks.namespaces import search_api
from estocks.models import StockExchangeMetaInfo

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
