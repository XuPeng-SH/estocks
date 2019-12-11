import logging
from datetime import datetime, date
from elasticsearch_dsl import Search, Document, Date, Integer, Keyword, Text, Q, MultiSearch, Index
from elasticsearch_dsl.query import MultiMatch, Match
from estocks import es_manager

logger = logging.getLogger(__name__)


META_EXCH_INDEX = Index('stock_exchange_meta_info')
META_STK_INDEX = Index('stock_meta_info')

@META_EXCH_INDEX.document
class StockExchangeMetaDoc(Document):
    id = Integer()
    display = Text(analyzer='snowball', fields={'raw': Keyword()})
    code = Text(analyzer='snowball', fields={'raw': Keyword()})
    area = Text(analyzer='snowball')
    country = Text(analyzer='snowball')

@META_STK_INDEX.document
class StockMetaDoc(Document):
    id = Integer()
    display = Text(analyzer='snowball', fields={'raw': Keyword()})
    area = Text(analyzer='snowball')
    industry = Text(analyzer='snowball')
    symbol = Text(analyzer='snowball')
    fullname = Text(analyzer='snowball')
    market = Text(analyzer='snowball')
    enname = Text(analyzer='snowball')
