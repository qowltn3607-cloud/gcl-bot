import os
import requests
from flask import Flask, request, jsonify
from estimator import extract_amount
from excel_manager import append_estimate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_URL   = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

TRIGGER_KEYWORDS = ["!견적", "견적", "추가", "달러", "불", "USD", "usd"]

def send_message(chat_id, text):
    requests.post(f"{TELEGRAM_URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

def is_estimate_message(msg: str) -> bool:
    return any(kw in msg for kw in TRIGGER_KEYWORDS)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}

    message_obj = data.get("message", {})
    message     = message_obj.get("text", "").strip()
    chat_id     = message_obj.get("chat", {}).get("id")
    sender      = message_obj.get("from", {}).get("first_name", "알 수 없음")

    if not message or not chat_id:
        return jsonify({"ok": True})

    if not is_estimate_message(message):
        return jsonify({"ok": True})

    amount = extract_amount(message)

    if amount is None:
        send_message(chat_id,
            "❌ 금액을 인식하지 못했어요.\n"
            "예시: '두바이 케이터링 추가 500달러' 또는 '방콕 스탭 연장 300불'"
        )
        return jsonify({"ok": True})

    no = append_estimate(sender=sender, message=message, amount=amount)

    send_message(chat_id,
        f"✅ 추가견적 #{no} 기록 완료!\n"
        f"👤 작성자: {sender}\n"
        f"💬 내용: {message}\n"
        f"💵 금액: ${amount:,.0f} USD"
    )
    return jsonify({"ok": True})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
