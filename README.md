# Web-Scraping-Automation-with-Cloud-Run-and-Scheduler

## Summary

This project uses **Python** and **Selenium** to automate the process of extracting exchange currency rates from [XE.com](https://www.xe.com). It runs on **Google Cloud Run** via **Docker**, with **Cloud Scheduler** triggering the process every minute. Data is stored in **Google Sheets**.  

## How it works

### Main.py

Access Google Spreadsheet.

Create a Chrome WebDriver.

Scrape exchange rate and datetime from XE.com.

Save data to Google Spreadsheet.

Provide a Flask endpoint to trigger the process.

### DockerFile

Build a Docker image with Python 3.10.

Install system dependencies, Google Chrome, and ChromeDriver.

Set environment variables for Chrome and ChromeDriver.

Copy the application code and credentials into the container.

Install Python dependencies.

Start the application with main.py.

## Setup

### Clone the repository:

```sh
git clone https://github.com/danielphan267/Web-Scraping-Automation-with-Cloud-Run-and-Scheduler.git
cd Web-Scraping-Automation-with-Cloud-Run-and-Scheduler
```

### Project Structure

```
/scraper-service
  ├── main.py
  ├── Dockerfile
  ├── requirements.txt
  ├── service-account.json
```

### Build and Push the Docker Image (Local Code)
1. Authenticate with Google Cloud

```sh
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

2. Enable Required Services

```sh
gcloud services enable run.googleapis.com containerregistry.googleapis.com
```

3. Build the Docker Image Locally

Run the following command from the project directory (where `Dockerfile` is located):

```sh
docker build -t gcr.io/YOUR_PROJECT_ID/scraper-service .
```

4. Push the Image to Google Container Registry (GCR)

```sh
gcloud auth configure-docker
docker push gcr.io/YOUR_PROJECT_ID/scraper-service
```

### Deploy to Google Cloud Run

Once the image is in GCR, deploy it directly:

```sh
gcloud run deploy scraper-service \
  --image gcr.io/YOUR_PROJECT_ID/scraper-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 300
```

### Google Cloud Scheduler

1. Enable Required Services

```sh
gcloud services enable run.googleapis.com cloudscheduler.googleapis.com
```

2. Create the Scheduler Job

```sh
gcloud scheduler jobs create http scraper-job \
  --schedule="*/1 * * * *" \
  --uri "https://scraper-service-xyz123-uc.a.run.app" \
  --http-method=GET \
  --time-zone="YOUR_TIME_ZONE" \
  --location="us-central1"
```

3. Run Scheduler Job

```sh
gcloud scheduler jobs run scraper-job --location="us-central1"
```




