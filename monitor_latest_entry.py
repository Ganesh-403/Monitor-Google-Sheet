import time
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os
import json
import logging

# Set up logging for debugging and monitoring
logging.basicConfig(level=logging.INFO)

def get_credentials():
    """Load and return Google Sheets API credentials from environment variable."""
    service_account_json = os.getenv("SERVICE_ACCOUNT_JSON")
    if not service_account_json:
        raise ValueError("The SERVICE_ACCOUNT_JSON environment variable is not set or is empty.")
    
    try:
        service_account_info = json.loads(service_account_json)
        return Credentials.from_service_account_info(service_account_info, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding SERVICE_ACCOUNT_JSON: {e}")

def get_sheet_client(credentials):
    """Authorize and return the gspread client."""
    try:
        return gspread.authorize(credentials)
    except Exception as e:
        raise ValueError(f"Error during authentication: {e}")

def check_latest_entry(client, sheet_name):
    """Fetch the latest entry from the specified Google Sheet."""
    try:
        logging.info(f"Checking latest entry for sheet: {sheet_name}")
        sheet = client.open(sheet_name).sheet1
        df = pd.DataFrame(sheet.get_all_records())  # Convert to DataFrame
        latest_entry = tuple(df.iloc[-1].values)  # Get the last row as a tuple
        logging.info(f"Latest entry: {latest_entry}")
        return latest_entry
    except gspread.exceptions.APIError as e:
        logging.error(f"API Error: {e}")
        return None

def monitor_spreadsheet():
    """Monitor the Google Sheet for new entries."""
    sheet_name = os.getenv("SHEET_NAME")
    if not sheet_name:
        raise ValueError("The SHEET_NAME environment variable is not set or is empty.")

    # Get credentials and authenticate client
    credentials = get_credentials()
    client = get_sheet_client(credentials)

    last_seen = None
    
    while True:
        latest_entry = check_latest_entry(client, sheet_name)

        if latest_entry and latest_entry != last_seen:
            logging.info("New entry detected:")
            logging.info(f"Entry: {latest_entry}")
            last_seen = latest_entry
        elif latest_entry is None:
            logging.warning("No new entry detected or unable to fetch data.")
        
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    logging.info("Starting the spreadsheet monitoring process...")
    monitor_spreadsheet()
