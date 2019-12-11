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
            from estocks.models import StockExchangeMetaInfo
            # from estocks import es_manager
            exchanges = StockExchangeMetaInfo.query.all()
            from estocks.documents import StockExchangeMetaDoc
            for exchange in exchanges:
                doc = StockExchangeMetaDoc(id=exchange.id,
                        display=exchange.display,
                        code=exchange.code,
                        area=exchange.area,
                        country=exchange.country)
                doc.save()


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
                                           StockExchangeMetaInfoFactory,
                                           StockDayDataFactory)
            db.drop_all()
            db.create_all()
            StockExchangeMetaInfoFactory(area='深圳',
                                       country='中国',
                                       display='深圳交易所',
                                       code='SZSE',
                                       short='SZ')
            StockExchangeMetaInfoFactory(area='上海',
                                       country='中国',
                                       display='上海交易所',
                                       code='SSE',
                                       short='SH')


    @staticmethod
    def register_stocks(yaml_path):
        app, db = Manager.init_app(yaml_path)
        import tushare as ts

        api = ts.pro_api('f3e484821271b2479be7885afa84b0be7f203209bcca903d890a4692')
        data = api.stock_basic(fields='ts_code,symbol,name,fullname,enname,area,industry,market,exchange,curr_type,is_hs,list_date,delist_date')
        cache = {}
        from estocks.models import StockExchangeMetaInfo
        from estocks.factories import StockMetaInfoFactory
        with app.app_context():
            for ind in data.index:
                ts_code, symbol, name, area, industry, market, \
                        list_date, delist_date, exchange,curr_type,fullname,enname,is_hs = data['ts_code'][ind], \
                        data['symbol'][ind], data['name'][ind], data['area'][ind], data['industry'][ind], \
                        data['market'][ind], data['list_date'][ind], data['delist_date'][ind], data['exchange'][ind], \
                        data['curr_type'][ind], data['fullname'][ind], data['enname'][ind], data['is_hs'][ind]
                print(ind, ts_code, symbol, name, area, industry, market, list_date, delist_date, exchange,curr_type,fullname,enname,is_hs)
                zone = ts_code.split('.')[1]
                exchange_key = exchange
                curr_exchange = cache.get(exchange_key, None)
                if not curr_exchange:
                    db_exchange = StockExchangeMetaInfo.query.filter_by(code=exchange).first()
                    cache[exchange_key] = db_exchange
                    curr_exchange = db_exchange

                db_stock = curr_exchange.stocks.filter_by(symbol=symbol).first()
                if not db_stock:
                    list_date = dt.datetime.strptime(list_date, "%Y%m%d")
                    delist_date = dt.datetime.strptime(delist_date, "%Y%m%d") if delist_date else None
                    StockMetaInfoFactory(exchange=curr_exchange, symbol=str(symbol),
                            industry=industry,
                            display=name,
                            is_hs=is_hs,
                            enname=enname,
                            curr_type=curr_type,
                            fullname=fullname,
                            area=area,
                            market=market,
                            delist_date=delist_date,
                            list_date=list_date)



if __name__ == '__main__':
    import fire
    fire.Fire(Manager)
