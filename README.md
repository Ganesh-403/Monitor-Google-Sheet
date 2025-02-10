# Monitor Google Sheets

## Overview
This project monitors a specified Google Sheet for new entries. It continuously checks for updates and logs any new records detected. The script uses the Google Sheets API to fetch data and integrates with GitHub Actions to run periodically.

## Features
- Monitors Google Sheets for new entries
- Logs latest detected records
- Uses Google Sheets API authentication
- Runs as a scheduled GitHub Action every minute
- Supports logging for debugging and tracking changes

## Requirements
Ensure you have the following installed:
- Python 3.9+
- Required dependencies (see `requirements.txt`)

## Installation & Setup

### 1. Clone the repository:
```
 git clone https://github.com/your-username/monitor-google-sheets.git
 cd monitor-google-sheets
```

### 2. Install dependencies:
```
pip install -r requirements.txt
```

### 3. Set up environment variables:
Create a `.env` file and add the following:
```
SERVICE_ACCOUNT_JSON=<your-service-account-json>
SHEET_NAME=<your-google-sheet-name>
```
Alternatively, set them in your shell:
```
export SERVICE_ACCOUNT_JSON='<your-service-account-json>'
export SHEET_NAME='<your-google-sheet-name>'
```

### 4. Run the script:
```
python monitor_latest_entry.py
```

## How It Works
1. The script retrieves credentials from the environment variable `SERVICE_ACCOUNT_JSON`.
2. It connects to the specified Google Sheet (`SHEET_NAME`).
3. It continuously checks for new entries every 60 seconds.
4. If a new entry is found, it logs the record.

## GitHub Actions Workflow
This project includes a GitHub Actions workflow (`.yml` file) to run the script every minute when pushed to the `main` branch.

### Workflow Breakdown
- Checks out the repository
- Sets up Python 3.9
- Installs dependencies
- Retrieves environment variables from GitHub Secrets
- Runs the script

### Adding Secrets to GitHub
Go to your repository settings -> Secrets -> Actions and add:
- `SERVICE_ACCOUNT_JSON`: Your Google service account JSON
- `SHEET_NAME`: The name of the Google Sheet to monitor

## Files Overview
- `monitor_latest_entry.py` - Main script for monitoring Google Sheets
- `requirements.txt` - Dependencies for the project
- `.gitignore` - Ignores sensitive files (e.g., service account JSON)
- `.github/workflows/monitor.yml` - GitHub Actions workflow file

## License
This project is licensed under the MIT License.

## Contributing
Feel free to submit issues and pull requests!

## Author
[Ganesh Kambli](https://github.com/Ganesh-403)

