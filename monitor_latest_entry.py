import json
import os
from google.oauth2 import service_account
import gspread

def check_latest_entry(sheet_name):
    service_account_info = json.loads(os.getenv("SERVICE_ACCOUNT_JSON"))
    credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(credentials)
    
    sheet = client.open(sheet_name).sheet1
    df = pd.DataFrame(sheet.get_all_records())
    
    return tuple(df.iloc[-1].values)  # Convert the last row to a tuple for comparison

def monitor_spreadsheet(sheet_name):
    last_seen = None
    
    while True:
        latest_entry = check_latest_entry(sheet_name)
        
        if latest_entry != last_seen:
            print("New entry detected:")
            print(latest_entry)
            last_seen = latest_entry

# Usage
sheet_name = input("Enter the name of the Google Sheet: ")
monitor_spreadsheet(sheet_name)
