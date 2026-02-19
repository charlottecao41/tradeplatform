class Signaller:
    def __init__(self, period : int = 63) -> void:
        self.period = period

    def riser(self, price: float, data: pd.DataFrame, increase_percentage: float = 1.3) -> bool:
        if data.sort_index().tail(self.period).iloc[-1]['close']*increase_percentage <= price:
            return True

        return False

    def tread(self, price: float, data: pd.DataFrame, period_length: int = 40, displacement: float = 0.25) -> bool:
        max_val = max(data.sort_index().tail(period_length)['close'])
        
        if (1-displacement)*max_val >= price and price <= (1-displacement)*max_val:
            return True

        return False

    def trigger(self, price: float, data: pd.DataFrame) -> bool:
        if price > max(data.sort_index().tail(self.period)['high']):
            print("Should buy.")
            return True

        return False

if  __name__ == "__main__":
    from backend.api.data_fetcher import DataFetcher
    data_fetcher = DataFetcher()
    signaller = Signaller()
    data = data_fetcher.get_data()
    print(signaller.riser(10, data))
    print(signaller.tread(10, data))
    print(signaller.trigger(10, data))

    
        