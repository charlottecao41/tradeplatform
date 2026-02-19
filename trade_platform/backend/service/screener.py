import pandas as pd

class Screener:
    def __init__(self, period : int = 50) -> void:
        self.period = period
        return

    def set_data(self, data: pd.Dataframe) -> void:
        self.data = data

    def liquidity_filter(self, price: float, data: pd.DataFrame, price_threshold:float = 3.00, average_volume:float = 300000 ) -> bool:
        volumn_ok = data.sort_index().tail(self.period)['volume'].mean() >= average_volume
        price_ok = price >= price_threshold
        if volumn_ok and price_ok:
            return True

        else:
            return False

    def trend_filter(self, price: float, data: pd.DataFrame,) -> bool:
        mean = data.sort_index().tail(self.period)['close'].mean()
        price = data.iloc[0]['close']
        if price > mean:
            return True

        else:
            return False


if  __name__ == "__main__":
    from backend.api.data_fetcher import DataFetcher
    data_fetcher = DataFetcher()
    screener = Screener()
    data = data_fetcher.get_data()
    print(screener.liquidity_filter(10, data))
    print(screener.trend_filter(10, data))