import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os
import json

def check_latest_entry(sheet_name):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    # Load service account credentials from GitHub secret
    service_account_info = json.loads(os.getenv("SERVICE_ACCOUNT_JSON"))
    credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    client = gspread.authorize(credentials)
    
    sheet = client.open(sheet_name).sheet1
    df = pd.DataFrame(sheet.get_all_records())
    return tuple(df.iloc[-1].values)

def monitor_spreadsheet(sheet_name):
    latest_entry = check_latest_entry(sheet_name)
    print("Latest entry in the spreadsheet:")
    print(latest_entry)

if __name__ == "__main__":
    sheet_name = os.getenv("SHEET_NAME")
    monitor_spreadsheet(sheet_name)
