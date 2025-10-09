from fastapi import FastAPI
import asyncio
import json
from datetime import datetime
import requests
from playwright.async_api import async_playwright

app = FastAPI()

# === Configuración de Telegram ===
TELEGRAM_TOKEN = "7810763269:AAHf0S69CfomW7fCF0UblDbDSfVYDyWPecE"
CHAT_ID = "7314372931"
NUMERO_WHATSAPP = "3132010072"

# === URLs de las páginas ===
URL_BULK = 'https://fabian0606.wixsite.com/streetfitness/rutinas'
URL_HYBRID = 'https://fabian0606.wixsite.com/streetfitness/crossfitness'

DIAS = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO"]

# === Función para enviar a Telegram ===
def enviar_telegram(mensaje: str):
    texto_url = requests.utils.quote(mensaje)
    enlace_whatsapp = f"https://wa.me/{NUMERO_WHATSAPP}?text={texto_url}"

    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "📲 Enviar por WhatsApp", "url": enlace_whatsapp}]
            ]
        }
    }

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("✅ Rutina enviada por Telegram correctamente.")
    else:
        print(f"⚠️ Error al enviar mensaje: {response.text}")

# === Función para extraer rutina ===
async def extraer_rutina(url: str, titulo: str):
    with open("cookies.json", "r") as f:
        cookies = json.load(f)
    for c in cookies:
        if "sameSite" not in c or c["sameSite"] not in ["Lax", "Strict", "None"]:
            c["sameSite"] = "Lax"

    dia_hoy = DIAS[datetime.now().weekday()]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(10000)

        texto_total = await page.evaluate("() => document.body.innerText")
        texto_total = texto_total.upper().replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")

        rutina_final = f"🏋️ RUTINA {titulo.upper()} {dia_hoy} 🏋️\n"

        if dia_hoy in texto_total:
            bloques = texto_total.split(dia_hoy)
            if len(bloques) > 1:
                siguiente_dia = next((d for d in DIAS if d in bloques[1]), None)
                rutina = bloques[1].split(siguiente_dia)[0] if siguiente_dia else bloques[1]
                lineas = [l.strip() for l in rutina.split("\n") if l.strip()]
                rutina_final += "\n".join(lineas[:80])
            else:
                rutina_final += f"No se encontró bloque de texto después del día {dia_hoy}"
        else:
            rutina_final += f"No se encontró texto con el día {dia_hoy}"

        await browser.close()

        return rutina_final


# === Endpoint principal ===
@app.get("/run")
async def run_rutinas():
    rutina_bulk = await extraer_rutina(URL_BULK, "BULK")
    rutina_hybrid = await extraer_rutina(URL_HYBRID, "HYBRID")

    mensaje = f"{rutina_bulk}\n\n=====================\n\n{rutina_hybrid}"

    enviar_telegram(mensaje)
    return {"status": "ok", "mensaje": "Rutinas enviadas correctamente 🚀"}
