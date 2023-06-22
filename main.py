import os
import requests
from datetime import datetime, timedelta
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "your virtual twilio number"
VERIFIED_NUMBER = "your own phone number verified with Twilio"

STOCK_NAME = "STOCK_NAME"
COMPANY_NAME = "COMPANY_NAME"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

NEWS_API_KEY = "YOUR OWN API KEY FROM NEWSAPI"
TWILIO_SID = "YOUR TWILIO ACCOUNT SID"
TWILIO_AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

api_key = os.environ.get("STOCK_API_KEY")
url = "https://www.alphavantage.co/query"
params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "datatype": "json",
    "apikey": api_key
}
response = requests.get(url, params=params)
data = response.json()

yesterday = str(datetime.now().date() - timedelta(1))
day_before = str(datetime.now().date() - timedelta(2))
days_data = data["Time Series (Daily)"]

for day, price in days_data.items():
    if yesterday == day:
        yesterday_stock_price = float(price["4. close"])
    if day_before == day:
        day_before_stock_price = float(price["4. close"])

difference = float(yesterday_stock_price) - float(day_before_stock_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterday_stock_price)) * 100)

if abs(diff_percent) >= 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: "
                          f"{article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )



