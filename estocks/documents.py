import logging
from datetime import datetime, date
from elasticsearch_dsl import Search, Document, Date, Integer, Keyword, Text, Q, MultiSearch, Index
from elasticsearch_dsl.query import MultiMatch, Match
from estocks import es_manager

logger = logging.getLogger(__name__)


INDEX = Index('stock_exchange_meta_info')

@INDEX.document
class StockExchangeMetaDoc(Document):
    id = Integer()
    display = Text(analyzer='snowball', fields={'raw': Keyword()})
    code = Text(analyzer='snowball', fields={'raw': Keyword()})
    area = Text(analyzer='snowball')
    country = Text(analyzer='snowball')

    # class Index:
    #     name = 'stock_exchange_meta_info'
