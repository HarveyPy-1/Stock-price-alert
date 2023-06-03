import requests
from datetime import datetime
import smtplib

# ------------------------------------ PARAMETERS ----------------------------------- #
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "JZMBQET692ISFZWO"
NEWS_API_KEY = "8e6b02466b3a4f0a833d8bf225410a11"
MY_EMAIL = "harveyezihe@gmail.com"
PASSWORD = "password"


# --------------------- CHECK THE DATE, ESPECIALLY MONTH AND DAY AS INTEGERS ---------------------- #
now = datetime.now()
now_str = str(now)
month = "{:02d}".format(int(now_str.split("-")[1]))
yesterday = "{:02d}".format(int(now_str.split("-")[2].split(" ")[0]) - 1)
day_before_yesterday = "{:02d}".format(int(now_str.split("-")[2].split(" ")[0]) - 2)
current_year = str(now.year)
current_month = "{:02d}".format(int(str(now.month)))
full_yesterday_string = str(now.day)
full_yesterday = "{:02d}".format(int(full_yesterday_string) - 1)
date = f"{current_year}-{current_month}-{full_yesterday}"

# ------------------------ GET THE CLOSING STOCK PRICE FOR THE PAST TWO DAYS ----------------------- #
stock_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": STOCK_API_KEY
}

stock_response = requests.get(url="https://www.alphavantage.co/query", params=stock_parameters)
stock_response.raise_for_status()
data = stock_response.json()
yesterday_closing_price = data["Time Series (Daily)"][f"2023-{month}-{yesterday}"]["4. close"]
day_before_yesterday_closing_price = data["Time Series (Daily)"][f"2023-{month}-{day_before_yesterday}"]["4. close"]
difference = (float(day_before_yesterday_closing_price) - float(yesterday_closing_price)) / float(day_before_yesterday_closing_price)

# ------------------------ GET THE NEWS FROM THE DAY BEFORE ----------------------- #
news_parameters = {
    "qInTitle": "Tesla",
    "from": date,
    "sortBy": "popularity",
    "apiKey": NEWS_API_KEY
}

news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()
news_title = news_data["articles"][0]["title"]
news_url = news_data["articles"][0]["url"]

# ------------------------ CHECK THE DIFFERENCE BETWEEN CLOSING PRICES AND SEND MAIL ----------------------- #
if (difference * 100) >= 5:
    diff_percent = "{:.0f}".format(round(difference * 100))
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="don4dolex@gmail.com",
            msg=f"Subject:STOCK ALERT! Tesla down {diff_percent}%\n\nNews Headline: " \
                f"{news_title}\n\nClick this link to read more: {news_url}"
        )
        print("Negative email sent!")

elif (difference * 100) < 0:
    diff_percent = "{:.0f}".format(round(difference * 100) * -1)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="my_email",
            msg=f"Subject:STOCK ALERT! Tesla up {diff_percent}%\n\nNews Headline: " \
                f"{news_title}\n\nClick this link to read more: {news_url}"
        )
        print("Positive email sent!")

