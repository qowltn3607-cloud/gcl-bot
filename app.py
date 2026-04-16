from flask import Flask, request, jsonify
from parser import extract_amount
from excel_manager import append_estimate
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

TRIGGER_KEYWORDS = ["!견적", "견적", "추가", "달러", "불", "USD", "usd"]

def is_estimate_message(msg: str) -> bool:
    return any(kw in msg for kw in TRIGGER_KEYWORDS)

@app.route("/webhook", methods=["POST"])
def webhook():
    data    = request.json or {}
    message = data.get("message", "").strip()
    sender  = data.get("sender", "알 수 없음")

    # 견적 관련 메시지가 아니면 무시
    if not is_estimate_message(message):
        return jsonify({"reply": None})

    # Claude로 금액 추출
    amount = extract_amount(message)

    if amount is None:
        reply = (
            "❌ 금액을 인식하지 못했어요.\n"
            "예시: '두바이 케이터링 추가 500달러' 또는 '!견적 방콕 스탭 연장 300'"
        )
        return jsonify({"reply": reply})

    # Excel에 기록
    no = append_estimate(sender=sender, message=message, amount=amount)

    reply = (
        f"✅ 추가견적 #{no} 기록 완료!\n"
        f"👤 작성자: {sender}\n"
        f"💬 내용: {message}\n"
        f"💵 금액: ${amount:,.0f} USD"
    )
    return jsonify({"reply": reply})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
