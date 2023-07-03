import csv
from datetime import datetime
import json
import os
import time
import requests
import telebot
from loguru import logger

OW_API = os.getenv("OW_API")
TG_BOT_API = os.getenv("TG_BOT_API")
CHAT_ID = os.getenv("CHAT_ID")


def get_weather() -> str | None:
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "Moscow",
        "appid": OW_API,
        "lang": "ru",
        "units": "metric"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        with open('icons.json', 'r', encoding='utf-8') as f:
            icons = json.load(f)
        text = f"Погода {icons[weather_data['weather'][0]['icon']]}: {int(weather_data['main']['temp'])}°C" \
               f" (ощ. {int(weather_data['main']['feels_like'])}°C), " \
               f"{weather_data['weather'][0]['description']}"
        logger.info(text)
        return text
    except (requests.RequestException, json.JSONDecodeError):
        logger.exception("Failed to get weather data")
        return None

def get_birthday() -> str:
    names = []
    with open("./birthdays.csv", "r") as file:
        csv_file = csv.DictReader(file)
        names = [line["Name"] for line in csv_file if line["date"] == f"{datetime.today().day}-{datetime.today().month}"]
    return "День рождения у 🎂: \n" + '\n'.join(names)


def create_message() -> str:
    return (
        "*Всем привет!👋*\n"
        f"{get_weather()}\n"
        f"{get_birthday()}\n"
    )


def send_message(text: str) -> None:
    bot = telebot.TeleBot(token=TG_BOT_API)
    bot.send_message(
        text=text,
        chat_id=CHAT_ID,
        disable_notification=True,
        parse_mode="markdown"
    )


def main() -> None:
    """
    This function is the main entry point of the program. It runs an infinite loop and checks if today is a weekday. If it is a weekday, it checks if the current time is 8:00 AM. If both conditions are true, it logs a message and sends a message by calling the create_message() function and passing the message to the send_message() function.

    Parameters: 
    None

    Returns: 
    None
    """
    while True:
        # check if today is monday-friday
        if datetime.now().weekday() < 5:
            if datetime.now().hour == 8 and datetime.now().minute == 0:
                logger.info("Sending message ")
                send_message(create_message())
        time.sleep(60)


if __name__ == '__main__':
    logger.info("Starting bot")
    main()
