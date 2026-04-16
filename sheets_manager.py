import os
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME     = "시트1"
CREDS_FILE     = "credentials.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def _get_service():
    creds = service_account.Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)

def setup_header():
    service = _get_service()
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

    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:A"
    ).execute()
    rows = result.get("values", [])
    no   = len(rows)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:E",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": [[no, now, sender, message, amount]]}
    ).execute()

    return no
