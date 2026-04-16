# GCL 추가견적 카카오톡 봇

출장 중 카카오톡 오픈채팅방에서 자연어로 말하면 Excel에 자동 기록되는 봇

## 파일 구조

```
gcl-bot/
  ├── app.py              # Flask 메인 서버
  ├── parser.py           # Claude API 금액 파싱
  ├── excel_manager.py    # Excel 기록
  ├── requirements.txt
  ├── Procfile            # Railway 배포용
  └── .env.example        # 환경변수 예시
```

## 환경변수 설정 (Railway Variables)

| 변수명 | 설명 |
|--------|------|
| `ANTHROPIC_API_KEY` | Anthropic API 키 |
| `KRW_RATE` | USD→KRW 환율 (기본: 1380) |

## 웹훅 요청 형식

```json
POST /webhook
{
  "message": "두바이 케이터링 추가 500달러 광고주 요청",
  "sender": "김나연"
}
```

## 응답 형식

```json
{
  "reply": "✅ 추가견적 #3 기록 완료!\n👤 작성자: 김나연\n💬 내용: ...\n💵 금액: $500 USD"
}
```
