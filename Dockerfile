FROM python:3.10

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Set Chrome environment variables
ENV CHROME_BIN="/usr/bin/google-chrome"
ENV CHROMEDRIVER_BIN="/usr/local/bin/chromedriver"

# Set working directory
WORKDIR /app

# Copy function code
COPY . .

# Copy the credentials JSON file into the container
COPY /service_account.json /app/service_account.json

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the application
CMD ["python", "main.py"]
