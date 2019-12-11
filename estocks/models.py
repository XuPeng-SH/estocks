import logging
import enum
from estocks import db
from estocks.base.models import SimpleModel

logger = logging.getLogger(__name__)


class StockExchangeMetaInfo(SimpleModel):
    __tablename__ = 'stock_exchange_meta_info'

    id = db.Column(db.Integer, primary_key=True)
    display = db.Column(db.String(50), nullable=False)
    short = db.Column(db.String(10), default="")
    code = db.Column(db.String(20), unique=True, index=True, nullable=False)
    area = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    extra = db.Column(db.JSON, default={})


class StockMetaInfo(SimpleModel):

    __tablename__ = 'stock_meta_info'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), index=True)
    display = db.Column(db.String(20), unique=True, nullable=False)
    fullname = db.Column(db.String(50), nullable=False)
    market = db.Column(db.String(20), nullable=False)
    enname = db.Column(db.String(128), nullable=False)
    exchange_id = db.Column(db.Integer, nullable=False)
    industry = db.Column(db.String(20), nullable=True)
    list_date = db.Column(db.Date, nullable=False)
    delist_date = db.Column(db.Date, default=None)
    list_status = db.Column(db.Integer, nullable=False)
    extra = db.Column(db.JSON, default={})
    is_hs = db.Column(db.String(2), default='N')
    curr_type = db.Column(db.String(10))
    area = db.Column(db.String(255), nullable=True)

    __table_args__ = (
        db.UniqueConstraint('symbol', 'exchange_id', name='_uc_stock_meta_info_symbol_exchange'),
    )

    exchange = db.relationship(
            StockExchangeMetaInfo,
            primaryjoin='and_(foreign(StockMetaInfo.exchange_id) == StockExchangeMetaInfo.id)',
            backref=db.backref('stocks', uselist=True, lazy='dynamic')
    )

    @property
    def ts_code(self):
        return f'{self.symbol}.{self.exchange.short}'


class StockDayData(SimpleModel):
    __tablename__ = 'stock_day_data'

    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    low = db.Column(db.Float)
    high = db.Column(db.Float)
    start = db.Column(db.Float)
    end = db.Column(db.Float)
    volume = db.Column(db.Float)

    __table_args__ = (
        db.UniqueConstraint('stock_id', 'date', name='_uc_stock_day_data_stock_date'),
    )

    stock = db.relationship(
        StockMetaInfo,
        primaryjoin='and_(foreign(StockDayData.stock_id) == StockMetaInfo.id)',
        backref=db.backref('days', uselist=True, lazy='dynamic')
    )
