from datetime import datetime, timezone
import pandas as pd

class Executor:
    def __init__(self, time_zone: timezone, risk: float = 100000, stop_distance = 14) -> None:
        self.buy_data = pd.DataFrame()
        self.tz = time_zone
        self.risk = risk
        self.stop_distance = stop_distance

    def receive_buy(self, price: float, time: datetime, volume: int, ticker: str) -> None:
        entry = pd.DataFrame([{'price': price, 'time': time.astimezone(self.tz), 'volume': volume, 'ticker': ticker}])
        self.buy_data = pd.concat([self.buy_data, entry], ignore_index=True)

    def sma(self, data: pd.DataFrame, day: int = 10) -> float:
        return data.sort_index().tail(day)['close'].mean()

    def risk_warn(self, price: float, volume: int, buy_price: float) -> bool:
        #fix risk
        if -1*(price - buy_price)*volume >= self.risk:
            return True 

        return False

    def stop_loss_warn(self, price: float, data: pd.DataFrame, buy_time: datetime) -> bool:
        #stop loss
        converted_buy_time = buy_time.astimezone(data.index.tz).floor('D')
        stop_loss = data.at[converted_buy_time, 'low']
        if price <= stop_loss:
            return True

        if buy_time - datetime.now(buy_time.tz)>=stop_distance:
            return True

        return False

    def exit_logic(self, price: float, data: pd.DataFrame) -> bool:

        #exit logic
        if price <= self.sma(data):
            return True

        return False

    def check_for_ticker(self, price: float, data: pd.DataFrame, ticker: str) -> None:
        if len(self.buy_data)==0:
            return
        to_check = self.buy_data[self.buy_data['ticker'] == ticker]
        for idx in range(len(to_check)):
            if self.risk_warn(price, volume = to_check['volume'].iloc[idx], buy_price = to_check['price'].iloc[idx]):
                print(f"{ticker} {to_check['time'].iloc[idx]}: Risk Warn")
            if self.stop_loss_warn(price, data,to_check['time'].iloc[idx]):
                print(f"{ticker} {to_check['time'].iloc[idx]}: Stop Loss Warn")
            if self.exit_logic(price, data):
                 print(f"{ticker} {to_check['time'].iloc[idx]}: Exit Warn")

if  __name__ == "__main__":
    from backend.api.data_fetcher import DataFetcher
    data_fetcher = DataFetcher()
    local = datetime.now(timezone.utc).astimezone().tzinfo
    executor = Executor(local)
    date_string = '2026-02-11'
    date = datetime.strptime(date_string, '%Y-%m-%d')
    data = data_fetcher.get_data()
    executor.receive_buy(10,date,1,'IBM')
    executor.check_for_ticker(10,data,'IBM')

