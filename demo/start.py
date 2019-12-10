import copy
import sys
import os
import datetime as dt
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(p)


class Manager:
    @staticmethod
    def server(*args, **kwargs):
        from estocks.cli import main
        main()

    @staticmethod
    def drop_table(*args, **kwargs):
        from estocks.cli import main
        main()

    @staticmethod
    def create_table(*args, **kwargs):
        from estocks.cli import main
        main()

    @staticmethod
    def mock_data(yaml_path, number=10):
        app, db = Manager.init_app(yaml_path)
        with app.app_context():
            from estocks.factories import StockMetaInfoFactory, StockMarketMetaInfoFactory, StockDayDataFactory
            markets = []
            markets.append(StockMarketMetaInfoFactory(area='上海'))
            markets.append(StockMarketMetaInfoFactory(area='深圳'))
            stocks = []
            for i in range(number):
                stocks.append(StockMetaInfoFactory(market=markets[i%2]))

            days = []
            for stock in stocks:
                s_days = StockDayDataFactory.create_batch(3, stock=stock)
                days.extend(s_days)
                print(stock.ts_code, stock.symbol, stock.display, stock.market.area)

    @staticmethod
    def init_app(yaml_path):
        from estocks import create_app, db
        app = create_app(yaml_path=yaml_path)

        return app, db

    @staticmethod
    def register_markets(yaml_path):
        app, db = Manager.init_app(yaml_path)
        with app.app_context():
            from estocks.factories import (StockMetaInfoFactory,
                                           StockMarketMetaInfoFactory,
                                           StockDayDataFactory)
            db.drop_all()
            db.create_all()
            StockMarketMetaInfoFactory(area='深圳',
                                       country='中国',
                                       display='中小板',
                                       short='SZ')
            StockMarketMetaInfoFactory(area='深圳',
                                       country='中国',
                                       display='创业板',
                                       short='SZ')
            StockMarketMetaInfoFactory(area='深圳',
                                       country='中国',
                                       display='主板',
                                       short='SZ')
            StockMarketMetaInfoFactory(area='上海',
                                       country='中国',
                                       display='主板',
                                       short='SH')
            StockMarketMetaInfoFactory(area='上海',
                                       country='中国',
                                       display='科创板',
                                       short='SH')


    @staticmethod
    def register_stocks(yaml_path):
        app, db = Manager.init_app(yaml_path)
        import tushare as ts

        api = ts.pro_api('f3e484821271b2479be7885afa84b0be7f203209bcca903d890a4692')
        data = api.stock_basic()
        market_cache = {}
        from estocks.models import StockMarketMetaInfo
        from estocks.factories import StockMetaInfoFactory
        with app.app_context():
            for ind in data.index:
                ts_code, symbol, name, area, industry, market, list_date = data['ts_code'][ind], \
                        data['symbol'][ind], data['name'][ind], data['area'][ind], data['industry'][ind], \
                        data['market'][ind], data['list_date'][ind]
                print(ind, ts_code, symbol, name, area, industry, market, list_date)

                zone = ts_code.split('.')[1]
                market_key = f'{zone}:{market}'
                curr_market = market_cache.get(market_key, None)
                if not curr_market:
                    db_market = StockMarketMetaInfo.query.filter_by(display=market, short=zone).first()
                    market_cache[market_key] = db_market
                    curr_market = db_market

                db_stock = curr_market.stocks.filter_by(symbol=symbol).first()
                if not db_stock:
                    list_date = dt.datetime.strptime(list_date, "%Y%m%d")
                    StockMetaInfoFactory(market=curr_market, symbol=str(symbol), industry=industry,
                            display=name, list_date=list_date)



if __name__ == '__main__':
    import fire
    fire.Fire(Manager)
