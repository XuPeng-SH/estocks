import logging
from estocks import db
from estocks.base.models import SimpleModel

logger = logging.getLogger(__name__)


class StockMarketMetaInfo(SimpleModel):
    __tablename__ = 'stock_market_meta_info'

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(50), unique=True, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    extra = db.Column(db.JSON, default={})


class StockMetaInfo(SimpleModel):
    __tablename__ = 'stock_meta_info'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), index=True)
    display_name = db.Column(db.String(50), unique=True, nullable=False)
    market_id = db.Column(db.Integer, nullable=False)
    extra = db.Column(db.JSON, default={})

    __table_args__ = (
        db.UniqueConstraint('code', 'market_id', name='_uc_stock_meta_info_code_market'),
    )

    market = db.relationship(
            StockMarketMetaInfo,
            primaryjoin='and_(foreign(StockMetaInfo.market_id) == StockMarketMetaInfo.id)',
            backref=db.backref('stocks', uselist=True, lazy='dynamic')
    )


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
