from backend.app import App

app = App(tickers=["IBM"], api_key="demo")
app.mock_run_once()
app.run()