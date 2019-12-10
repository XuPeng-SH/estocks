import copy
import sys
import os
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
        from estocks import create_app, db
        app = create_app(yaml_path=yaml_path)
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


if __name__ == '__main__':
    import fire
    fire.Fire(Manager)
