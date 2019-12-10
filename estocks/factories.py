import factory
from factory.alchemy import SQLAlchemyModelFactory
from estocks import db
from estocks.models import (StockMarketMetaInfo, StockDayData, StockMetaInfo)

class StockMarketMetaInfoFactory(SQLAlchemyModelFactory):
    class Meta:
        model = StockMarketMetaInfo
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    display_name = factory.Faker('word')
    location = factory.Iterator(['Shanghai', 'ShenZhen'])


class StockMetaInfo(SQLAlchemyModelFactory):
    class Meta:
        model = StockMetaInfo
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    market = factory.SubFactory(StockMarketMetaInfoFactory)
    code =  factory.Faker('random_number', digits=6, fix_len=True)
    display_name = factory.Faker('word')
    location = factory.Iterator(['Shanghai', 'ShenZhen'])
