from alpaca_trade_api.rest import REST
from dotenv import load_dotenv
import pandas as pd
import chart
import config
import os
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL")

print(f"Capital disponible: ${config.CAPITAL}")
print(BASE_URL)

api = REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

ticker = config.TICKER
timeframe = config.TIMEFRAME
start_date = config.START_DATE
end_date = config.END_DATE

# Las cripto usan otro endpoint (get_crypto_bars) y no necesitan feed.
# Las acciones/ETFs usan get_bars con el feed configurado (iex/sip).
es_cripto = "/" in ticker

if es_cripto:
    data = api.get_crypto_bars(ticker, timeframe, start=start_date, end=end_date).df
else:
    data = api.get_bars(ticker, timeframe, start=start_date, end=end_date,
                        feed=config.FEED).df

print("✅ Datos recibidos:")
print(f"Ticker: {ticker} | Timeframe: {timeframe}")
print("Número de registros:", len(data))
print(data)

if data.empty:
    print("⚠️  Sin datos para ese rango (¿fin de semana, festivo o fechas en el futuro?).")
    print("    No se sobrescribe el CSV ni se genera gráfico.")
else:
    # Guardar los datos en /data como CSV (crea la carpeta si no existe)
    os.makedirs("data", exist_ok=True)
    nombre_csv = "".join(c if c.isalnum() else "_" for c in f"{ticker}_{timeframe.value}")
    ruta_csv = f"data/{nombre_csv}.csv"
    data.to_csv(ruta_csv)
    print(f"💾 Datos guardados en: {ruta_csv}")

    chart.graficar_precio(data, titulo=f"{ticker} ({timeframe.value}) - Precio de cierre",
                          nombre_archivo=nombre_csv)




