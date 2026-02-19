from datetime import timezone, datetime
import schedule
from backend.api.data_fetcher import DataFetcher
from backend.service.screener import Screener
from backend.service.signaller import Signaller
from backend.service.executor import Executor

class App:

    def __init__(self, tickers: []=['IBM'], api_key: str="demo", time_zone: timezone=datetime.now(timezone.utc).astimezone().tzinfo) -> void:
        self.data_fetcher = DataFetcher(api_key)
        self.screener = Screener()
        self.executor = Executor(time_zone)
        self.signaller = Signaller()
        self.tickers = tickers
        self.cached_data = {}
        for ticker in tickers:
            self.cached_data.update({ticker: None})

    def respond_to_price(self, price: float, ticker: str="IBM") -> void:
        if self.screener.liquidity_filter(price, self.cached_data[ticker]) and self.screener.trend_filter(price, self.cached_data[ticker]):
                if self.signaller.riser(price, self.cached_data[ticker]) and self.signaller.tread(price, self.cached_data[ticker]) and self.signaller.trigger(price,self.cached_data[ticker]):
                    volume = int(input("Volume of Buy"))
                    if volume > 0:
                        buy_time = datetime.now(executor.tz)
                        self.executor.receive_buy(price, buy_time, volume, ticker)

        self.executor.check_for_ticker(price,self.cached_data[ticker],ticker)

    def run_once(self):
        for ticker in self.tickers:
            if self.cached_data[ticker] is None:
                self.cached_data[ticker] = self.data_fetcher.get_data(ticker)
            
            print(f"Fetching {ticker} data...")
            price = self.data_fetcher.get_current_price(ticker)
            self.respond_to_price(price, ticker)


    def set_historical():
        for ticker in self.tickers:
            self.cached_data[ticker] = self.data_fetcher.get_data(ticker)
        print("Setting historical data...")

    def run(self, interval: int = 5):
        schedule.every().day.at("00:00").do(self.set_historical)
        schedule.every(interval).minutes.do(self.run_once)
        while True:
            schedule.run_pending()

    def mock_run_once(self):
        price = self.data_fetcher.get_current_price()
        data = self.data_fetcher.get_data()
        print("screener liquidity response: ", self.screener.liquidity_filter(price, data))
        print("screener screener response: ", self.screener.trend_filter(price, data))
        print("signaller riser reponse: ", self.signaller.riser(price, data))
        print("signaller tread reponse: ", self.signaller.tread(price, data))
        print("signaller trigger reponse: ", self.signaller.trigger(price, data))
        print("---Mock buy volume = 10 @ 2026-02-11---")
        date_string = '2026-02-11'
        date = datetime.strptime(date_string, '%Y-%m-%d')
        print("executor response")
        self.executor.check_for_ticker(price,data,ticker='IBM')

if __name__ == "__main__":
    app = App()
    #app.run()
    app.mock_run_once()