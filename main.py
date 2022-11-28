from __future__ import annotations

import csv
import json
import os

import requests
import telebot
from datetime import datetime

OW_API = os.getenv("OW_API")


def get_weather() -> str | None:
    """
    Request weather from openWeatherApi and format
    :return: str if ok, else None
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Moscow&appid={OW_API}&lang=ru&units=metric"
    weather_data = requests.get(url)
    with open('icons.json', 'r', encoding='utf-8') as f:
        icons = json.load(f)
    print(weather_data.status_code)
    if weather_data.status_code == 200:
        weather_data = weather_data.json()
        text = f"Погода {icons[weather_data['weather'][0]['icon']]}: {weather_data['main']['temp']}°C" \
               f" (ощ. {weather_data['main']['feels_like']}°C), " \
               f"{weather_data['weather'][0]['description']}"
        return text
    else:
        return None


def get_birthday() -> str | None:
    """
    Read birthday csv file in format "Name", "DD-MM"
    :return: return Name or None
    """
    names = []
    with open("./birthdays.csv", "r") as file:
        csv_file = csv.DictReader(file)
        for line in csv_file:
            if line["date"] == f"{datetime.today().day}-{datetime.today().month}":
            # if line['date'] == "04-02":
                names.append(line["Name"])
    if len(names) == 0:
        return None
    else:
        return '\n'.join(names)


def main() -> None:
    print("Heello world!")
    print(get_weather())
    print(get_birthday())


if __name__ == '__main__':
    main()
