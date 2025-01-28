import time
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os
import json

def check_latest_entry():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    # Load service account credentials from environment variable
    service_account_json = os.getenv("SERVICE_ACCOUNT_JSON")
    if not service_account_json:
        raise ValueError("The SERVICE_ACCOUNT_JSON environment variable is not set or is empty.")
    
    try:
        service_account_info = json.loads(service_account_json)
        credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding SERVICE_ACCOUNT_JSON: {e}")

    # Authenticate with Google Sheets API
    try:
        client = gspread.authorize(credentials)
    except Exception as e:
        raise ValueError(f"Error during authentication: {e}")

    # Get the sheet name from environment variable
    sheet_name = os.getenv("SHEET_NAME")
    if not sheet_name:
        raise ValueError("The SHEET_NAME environment variable is not set or is empty.")
    
    retries = 5  # Number of retry attempts
    backoff_time = 1  # Initial backoff time in seconds

    # Retry logic in case of quota limit or other temporary errors
    for attempt in range(retries):
        try:
            # Open the sheet by name and get the last entry
            sheet = client.open(sheet_name).sheet1
            df = pd.DataFrame(sheet.get_all_records())  # Convert to DataFrame
            return tuple(df.iloc[-1].values)  # Get the last row as a tuple
        except gspread.exceptions.APIError as e:
            # Handle quota exceeded error and retry with exponential backoff
            if e.response.status_code == 429:  # Quota exceeded error
                print(f"Quota exceeded, retrying... Attempt {attempt + 1}/{retries}")
                time.sleep(backoff_time)  # Wait before retrying
                backoff_time *= 2  # Exponential backoff
            else:
                # Raise other API-related errors
                raise e
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None  # Return None if any other errors occur

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
        elif latest_entry is None:
            print("No new entry detected or unable to fetch data.")
        
        time.sleep(check_interval)

# Main function entry point, with environment variables
if __name__ == "__main__":
    monitor_spreadsheet(check_interval=60)
