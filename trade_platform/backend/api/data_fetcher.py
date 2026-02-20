import requests
import pandas as pd

class DataFetcher:
    def __init__(self, api_key: str="demo") -> None:
        self.api = api_key


    def get_data(self, ticker: str="IBM", full_output: bool = False) -> pd.DataFrame:
        if full_output:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={self.api}'
        else:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={self.api}'
        r = requests.get(url)
        data = r.json()
        time_zone = data["Meta Data"]["5. Time Zone"]
        df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient='index')
        df.index = pd.to_datetime(df.index)
        df.index = df.index.tz_localize(time_zone) 
        df = df.sort_index()
        df.columns = [col.split('. ')[1] for col in df.columns]
        df = df.apply(pd.to_numeric)
        return df

    def get_current_price(self, ticker: str="IBM") -> float:
        #there should be a current price api implementation here
        #I don have access so I will let it return a fixed number for now

        return 10000

if __name__ == "__main__":
    data_fetcher = DataFetcher()
    print(data_fetcher.get_data())
