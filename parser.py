import anthropic
import os
import json
import re

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """
너는 출장 현장 추가 견적 메시지에서 금액(USD)만 추출하는 봇이야.

규칙:
- 메시지에서 USD 금액 숫자만 추출해서 JSON으로 반환해
- 통화 표기가 없으면 USD로 간주해
- 금액이 없거나 견적과 무관한 메시지면 null 반환
- 반드시 아래 형식으로만 응답해 (다른 말 금지)

{"amount": 500} 또는 {"amount": null}
"""

def extract_amount(message: str) -> float | None:
    try:
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=100,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": message}]
        )
        text = resp.content[0].text.strip()
        # ```json 블록 제거
        text = re.sub(r"```json|```", "", text).strip()
        data = json.loads(text)
        return data.get("amount")
    except Exception:
        return None
