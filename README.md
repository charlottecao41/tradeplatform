# Quickstart
```bash
cd trade_platform
python test.py
```

# Usage

```python
from backend.app import App
app = App(tickers=["IBM"], api_key="your_api_key")
app.run(interval=5)
```

Every day, this fetches historical data for all tickers once. Then every 5 minutes it will fetch the current data (api to be implemented depending on your data source), and prompt the user to buy or sell.

# Answering Qns

API: Used Alpha vantage, as there is a free demo key for testing. Limitation: real time data requires premium key, which cannot be tested

System Review:
1.	Data Structure: Pandas, since it is easily readable & fast
2.	Modularity: separated screener, signaller, executor and api
3.	Trade-off: executor should have a sql data base to store the buy data & query as needed, but I don’t have time so I used a pandas dataframe instead; Should also include unit tests & other CD/CI tools, but I have no time.
4.	To be improved
a.	The moving average is used a lot of time, instead of calculating by reading the entirely list & find average, we can use (the previous average * period – last data point + new day’s data)/period instead
5.	Lacking
a.	Did not implement: Get current data api, trading action
b.	Too many tickers & longer data windows will eat up ram
