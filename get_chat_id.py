import httpx
import time

TOKEN = "8576656133:AAG_eS6tLIk6joYiZT1BI1IppF0htS2X7sQ"
URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

print("Buscando mensajes enviados al bot...\n")

try:
    response = httpx.get(URL, timeout=10)
    data = response.json()

    if not data.get("result"):
        print("No hay mensajes aún. Envía 'hola' a @vaga_curitiba_bot en Telegram y vuelve a ejecutar este script.")
    else:
        for update in data["result"]:
            msg = update.get("message")
            if msg:
                chat_id = msg["chat"]["id"]
                name = msg["chat"].get("first_name", "")
                print(f"✅ Chat ID encontrado: {chat_id}")
                print(f"   Nombre: {name}")
                print(f"\nCrea el archivo .env con este contenido:")
                print(f"BOT_TOKEN={TOKEN}")
                print(f"CHAT_ID={chat_id}")
                break
except Exception as e:
    print(f"Error: {e}")
