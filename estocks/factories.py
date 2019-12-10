import factory
import random
from factory.alchemy import SQLAlchemyModelFactory
from faker.providers import BaseProvider
import datetime
from estocks import db
from estocks.models import (StockMarketMetaInfo, StockDayData, StockMetaInfo)


class MyProvider(BaseProvider):
    def my_date(self):
        return datetime.datetime.today() - datetime.timedelta(days=random.randint(0, 100))

factory.Faker.add_provider(MyProvider)


class StockMarketMetaInfoFactory(SQLAlchemyModelFactory):
    class Meta:
        model = StockMarketMetaInfo
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    display_name = factory.Faker('word')
    location = factory.Faker('random_element', elements=('Shanghai', 'ShenZhen'))


class StockMetaInfoFactory(SQLAlchemyModelFactory):
    class Meta:
        model = StockMetaInfo
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    market = factory.SubFactory(StockMarketMetaInfoFactory)
    code =  factory.Faker('random_number', digits=6, fix_len=True)
    display_name = factory.Faker('word')


class StockDayDataFactory(SQLAlchemyModelFactory):
    class Meta:
        model = StockDayData
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    stock = factory.SubFactory(StockMetaInfoFactory)
    date = factory.Faker('my_date')
    low = factory.Faker('random_number', digits=6, fix_len=True)
    high = factory.Faker('random_number', digits=8, fix_len=True)
    start = factory.Faker('random_number', digits=7, fix_len=True)
    end = factory.Faker('random_number', digits=7, fix_len=True)
