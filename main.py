from google.cloud import secretmanager
from flask import Flask, request, jsonify
from datetime import datetime
import pytz
from markupsafe import escape
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

# Google Sheets Constants
SPREADSHEET_ID = "google_sheet_id"  # Replace with your Google Sheet ID
                  
RANGE_NAME = "Sheet1!A2"  # Update the range as needed

# Function to scrape exchange rate
def scrape_exchange_rate():
    # URL and Selenium setup
    url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=VND'

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        driver.refresh()
        driver.implicitly_wait(2)

        # Scrape data
        element_rate = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[5]/div[2]/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[1]')
        element_date = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[5]/div[2]/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]')
        rate_text = element_rate.text
        time_text = element_date.text
        
        # Parse rate and timestamp
        rate = rate_text.split()[4]
        utc_time = datetime.strptime(time_text[55:-4], '%b %d, %Y, %H:%M')
        utc = pytz.timezone('UTC')
        utc_time = utc.localize(utc_time)

        return {
            "rate": rate,
            "time": utc_time.isoformat(),
        }
    finally:
        driver.quit()

# Function to upload data to Google Sheets
def upload_to_google_sheets(data):
    creds = service_account.Credentials.from_service_account_file(
        '/app/service_account.json', scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=creds)

    values = [[data["rate"], data["time"]]]
    body = {"values": values}

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption="RAW",
        body=body
    ).execute()

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def run_scraper():
    data = scrape_exchange_rate()
    upload_to_google_sheets(data)
    return jsonify({"message": "Data scraped and uploaded successfully!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)