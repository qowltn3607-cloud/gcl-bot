import os
import json
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME     = "시트1"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def _get_service():
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    creds_dict = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)

def setup_header():
    service = _get_service()
    # 헤더가 없으면 생성
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A1:E1"
    ).execute()

    if not result.get("values"):
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A1:E1",
            valueInputOption="RAW",
            body={"values": [["No", "접수일시", "작성자", "내용 (자연어 그대로)", "금액 (USD)"]]}
        ).execute()

def append_estimate(sender: str, message: str, amount: float) -> int:
    service = _get_service()

    # 현재 행 수 확인
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:A"
    ).execute()
    rows = result.get("values", [])
    no   = len(rows)  # 헤더 제외한 데이터 행 수 = NO

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:E",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": [[no, now, sender, message, amount]]}
    ).execute()

    return no
