import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "kz_verify_2026")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@app.get("/webhook")
def verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)
    return PlainTextResponse("Verification failed", status_code=403)


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]["value"]

        if "messages" in changes:
            msg = changes["messages"][0]
            from_number = msg["from"]
            text = msg["text"]["body"]

            reply = ask_openai(text)
            send_whatsapp_message(from_number, reply)

    except Exception as e:
        print("Webhook Error:", e)

    return {"status": "ok"}


def ask_openai(user_text: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Сен қазақ тілінде жауап беретін бизнес-ассистентсің. "
                    "Қысқа, нақты, сыпайы жауап бер."
                ),
            },
            {"role": "user", "content": user_text},
        ],
        "temperature": 0.4,
    }

    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def send_whatsapp_message(to: str, text: str):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }

    r = requests.post(url, headers=headers, json=payload)
    print("WhatsApp response:", r.text)
