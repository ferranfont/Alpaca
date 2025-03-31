from alpaca_trade_api.rest import REST, TimeFrame
from dotenv import load_dotenv
import pandas as pd

import chart

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL")

print(f"Capital disponible: ${config.CAPITAL}")
print(BASE_URL)

from alpaca_trade_api.rest import REST
api = REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

from alpaca_trade_api.rest import TimeFrame


#data = api.get_bars("AAPL", TimeFrame.Day, limit=30, feed="iex").df
# data = api.get_crypto_bars(config.TICKER, TimeFrame.Minute, limit=150).df  #solo crytpos

start_date = pd.Timestamp("2022-02-01", tz="America/New_York").isoformat()
end_date = pd.Timestamp("2025-03-29", tz="America/New_York").isoformat()

data = api.get_bars("TSLA", TimeFrame.Day, start=start_date, end=end_date).df

#data = api.get_bars(config.TICKER, TimeFrame.Minute, limit=550).df


print("✅ Datos recibidos:")
print(len(data))
print(data)



# Asumiendo que ya tienes el DataFrame `data`
chart.graficar_precio(data, titulo=f"{config.TICKER} - Precio de cierre")




