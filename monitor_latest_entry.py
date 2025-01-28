import time
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os
import random

def check_latest_entry():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    # Load the service account credentials
    credentials = Credentials.from_service_account_file("path/to/your/service_account.json", scopes=SCOPES)
    client = gspread.authorize(credentials)
    
    sheet_name = os.getenv("SHEET_NAME")  # Get the sheet name from the environment variable
    
    if not sheet_name:
        raise ValueError("The SHEET_NAME environment variable is not set")
    
    retries = 5  # Number of retry attempts
    backoff_time = 1  # Initial backoff time in seconds

    for attempt in range(retries):
        try:
            sheet = client.open(sheet_name).sheet1  # Open the sheet by name
            df = pd.DataFrame(sheet.get_all_records())  # Convert to DataFrame
            return tuple(df.iloc[-1].values)  # Get the last row as a tuple
        except gspread.exceptions.APIError as e:
            if e.response.status_code == 429:  # Quota exceeded error
                print(f"Quota exceeded, retrying... Attempt {attempt + 1}/{retries}")
                time.sleep(backoff_time)  # Wait before retrying
                backoff_time *= 2  # Exponential backoff
            else:
                raise e
    print("Max retry attempts reached. Quota still exceeded.")
    return None  # Return None if retries are exhausted

def monitor_spreadsheet(check_interval=60):
    last_seen = None
    
    while True:
        latest_entry = check_latest_entry()
        
        if latest_entry and latest_entry != last_seen:
            print("New entry detected:")
            print(latest_entry)
            last_seen = latest_entry
        
        time.sleep(check_interval)

# Usage: Set the environment variable before running
# SHEET_NAME=<your-google-sheet-name> python monitor_latest_entry.py
monitor_spreadsheet()
