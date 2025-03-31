from alpaca_trade_api.rest import REST
from dotenv import load_dotenv
import os

load_dotenv()

api = REST(
    os.getenv("API_KEY"),
    os.getenv("API_SECRET"),
    os.getenv("BASE_URL"),
    api_version="v2"
)

try:
    account = api.get_account()
    print(f"✅ Conectado correctamente como: {account.status}")
    print(f"💰 Equity: {account.equity}")
except Exception as e:
    print("❌ ERROR de autenticación:", e)

account = api.get_account()
print(account)


from alpaca_trade_api.rest import REST, TimeFrame
from dotenv import load_dotenv
import os
import pandas as pd

# Cargar claves desde .env
load_dotenv()

api = REST(
    os.getenv("API_KEY"),
    os.getenv("API_SECRET"),
    os.getenv("BASE_URL"),
    api_version="v2"
)

# 🔁 Descargar barras diarias (últimos 30 días) con feed IEX
try:
    df = api.get_bars("SPX", TimeFrame.Day, limit=30, feed="iex").df
    if df.empty:
        print("⚠️ No se obtuvieron datos. ¿Activaste el feed IEX en tu cuenta?")
    else:
        print("✅ Datos diarios de AAPL:")
        print(df.head())

        # 📝 Guardar CSV
        output_path = "DATA/AAPL_daily.csv"
        os.makedirs("DATA", exist_ok=True)
        #df.to_csv(output_path)
        print(f"📁 Guardado como: {output_path}")
except Exception as e:
    print("❌ Error al obtener datos:")
    print(e)