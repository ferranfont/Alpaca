"""
main_realtime.py
----------------
Datos en TIEMPO REAL desde Alpaca usando WebSocket (clase Stream).

A diferencia de main.py (que usa REST para datos HISTÓRICOS),
aquí abrimos una conexión permanente: nos suscribimos a un instrumento
y Alpaca nos "empuja" cada nuevo dato (trade, quote o barra) en cuanto ocurre.

Para parar el stream: Ctrl + C
"""

from alpaca_trade_api.stream import Stream
from dotenv import load_dotenv
import chart_realtime
import config
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

ticker = config.TICKER
es_cripto = "/" in ticker

# data_feed: "iex" (gratis) o "sip" (pago) para acciones. La cripto usa su propio feed.
stream = Stream(
    API_KEY,
    API_SECRET,
    data_feed=config.FEED,   # se ignora para cripto
    raw_data=False,
)

# La librería alpaca-trade-api (3.2.0, descontinuada) apunta el WebSocket de cripto
# a /v1beta2/crypto, un endpoint que Alpaca ya retiró (da HTTP 404).
# Lo forzamos al actual: /v1beta3/crypto/us
if es_cripto:
    stream._crypto_ws._endpoint = "wss://stream.data.alpaca.markets/v1beta3/crypto/us"


# ---- Handlers: funciones async que se ejecutan cada vez que llega un dato ----

async def on_trade(t):
    # Una operación ejecutada en el mercado
    print(f"💹 TRADE  {t.symbol}  precio={t.price}  size={t.size}  @ {t.timestamp}")


async def on_quote(q):
    # Mejor oferta de compra (bid) y venta (ask) en ese instante
    print(f"📊 QUOTE  {q.symbol}  bid={q.bid_price} x{q.bid_size}  "
          f"ask={q.ask_price} x{q.ask_size}  @ {q.timestamp}")
    # Enviamos el bid al gráfico en vivo del navegador
    chart_realtime.add_bid(q.timestamp, q.bid_price)


async def on_bar(b):
    # Barra OHLCV cerrada (llega una por minuto)
    print(f"🕐 BAR    {b.symbol}  O={b.open} H={b.high} L={b.low} "
          f"C={b.close} V={b.volume}  @ {b.timestamp}")


# ---- Suscripciones: cripto y acciones usan métodos distintos ----

if es_cripto:
    stream.subscribe_crypto_trades(on_trade, ticker)
    stream.subscribe_crypto_quotes(on_quote, ticker)
    stream.subscribe_crypto_bars(on_bar, ticker)
else:
    stream.subscribe_trades(on_trade, ticker)
    stream.subscribe_quotes(on_quote, ticker)
    stream.subscribe_bars(on_bar, ticker)


if __name__ == "__main__":
    # Arranca el gráfico en vivo en el navegador (servidor web en hilo aparte)
    chart_realtime.start_dashboard(ticker)

    print(f"🔌 Conectando al stream en tiempo real de {ticker} "
          f"({'cripto' if es_cripto else 'acción/' + config.FEED})...")
    print("   (Ctrl + C para detener)\n")
    try:
        stream.run()
    except KeyboardInterrupt:
        print("\n👋 Stream detenido por el usuario.")
