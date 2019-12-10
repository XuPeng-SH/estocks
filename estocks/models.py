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

    code = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(50), unique=True, nullable=False)
    market_id = db.Column(db.Integer, nullable=False)
    extra = db.Column(db.JSON, default={})

    market = db.relationship(
            StockMarketMetaInfo,
            primaryjoin='and_(foreign(StockMetaInfo.market_id) == StockMarketMetaInfo.id)',
            backref=db.backref('stocks', uselist=True, lazy='dynamic')
    )


class StockDayData(SimpleModel):
    __tablename__ = 'stock_day_data'

    code = db.Column(db.Integer, primary_key=True)
