# Quickstart
python test.py

# Usage

```python
from backend.app import App
app = App(tickers=["IBM"], api_key="your_api_key")
app.run(interval=5)
```

Every day, this fetches historical data for all tickers once. Then every 5 minutes it will fetch the current data (api to be implemented depending on your data source), and prompt the user to buy or sell.
