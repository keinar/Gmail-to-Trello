FROM mcr.microsoft.com/playwright/python:v1.57.0-jammy

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 

RUN apt-get update && \
    apt-get install -y default-jre wget unzip && \
    apt-get clean

RUN wget https://github.com/allure-framework/allure2/releases/download/2.36.0/allure-2.36.0.zip && \
    unzip allure-2.36.0.zip -d /opt/ && \
    ln -s /opt/allure-2.36.0/bin/allure /usr/bin/allure && \
    rm allure-2.36.0.zip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs allure-results

CMD sh -c "rm -rf allure-results/* && pytest --alluredir=allure-results --junitxml=/app/logs/pytest-results.xml"