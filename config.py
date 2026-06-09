#variables del sistema
from pandas import Timestamp
from alpaca_trade_api.rest import TimeFrame, TimeFrameUnit

CAPITAL = 3000
TIMEFRAME =59
TICKER = "BTC/USD"
#TICKER = "AAPL"

START_DATE = Timestamp("2026-06-04", tz="America/New_York").isoformat()
END_DATE = Timestamp("2026-06-06", tz="America/New_York").isoformat()

# ---- Configuración de datos intradiarios ----
# Cambia TIMEFRAME por el que quieras:
#   TimeFrame.Minute                          -> 1 minuto
#   TimeFrame(5, TimeFrameUnit.Minute)        -> 5 minutos
#   TimeFrame(15, TimeFrameUnit.Minute)       -> 15 minutos
#   TimeFrame.Hour                            -> 1 hora
#   TimeFrame.Day                             -> diario
TIMEFRAME = TimeFrame(TIMEFRAME, TimeFrameUnit.Minute)

# Feed de datos para acciones/ETFs:
#   "iex" -> gratis (cobertura parcial)
#   "sip" -> consolidado (requiere suscripción de pago)
FEED = "iex"


