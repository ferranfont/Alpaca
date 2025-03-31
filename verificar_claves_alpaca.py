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