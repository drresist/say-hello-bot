import os
import json
import requests
import telegram
import datetime
from typing import List
from loguru import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from telegram.ext import Updater, JobQueue, CallbackContext, CallbackQueryHandler

WEATHER_API_KEY = os.getenv("OW_API")
TELEGRAM_BOT_TOKEN = os.getenv("TG_BOT_API")
CHAT_ID = os.getenv("CHAT_ID")

ICONS = {}
with open("icons.json", "r", encoding="utf-8") as f:
    ICONS = json.load(f)


def get_weather_data() -> str:
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": "Moscow", "appid": WEATHER_API_KEY, "lang": "ru", "units": "metric"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        return f"Погода {ICONS[weather_data['weather'][0]['icon']]}: {int(weather_data['main']['temp'])}°C (ощ. {int(weather_data['main']['feels_like'])}°C), {weather_data['weather'][0]['description']}"
    except Exception as e:
        logger.error(f"Failed to get weather data: {e}")
        return ""


def send_weather_message(context: CallbackContext) -> None:
    weather_data = get_weather_data()
    keyboard = [[InlineKeyboardButton("+1", callback_data="add_one")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

    bot.send_message(chat_id=CHAT_ID, text=weather_data, reply_markup=reply_markup)


def add_one_callback(update: Update, context: CallbackContext) -> None:
    if not update.callback_query.from_user.id in context.user_data:
        user = update.callback_query.from_user
        logger.info(f"Button pressed by user {user.full_name} - {user.id}")
        context.user_data[update.callback_query.from_user.id] = True


def send_report_message(context: CallbackContext) -> None:
    report_message = f"Проснулись: {len(context.user_data.keys())} человек"
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

    keyboard = [
        [InlineKeyboardButton("Send report again", callback_data="resend_report")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = bot.send_message(
        chat_id=CHAT_ID, text=report_message, reply_markup=reply_markup
    )
    context.user_data.clear()


def restart_handler(update: Update, context: CallbackContext) -> None:
    send_report_message(context)


def schedule_jobs(updater: Updater) -> JobQueue:
    job_queue = updater.job_queue

    job_queue.run_daily(send_weather_message, time=datetime.time(8, 0, 0))
    job_queue.run_daily(send_report_message, time=datetime.time(9, 15, 0))
    updater.dispatcher.add_handler(CallbackQueryHandler(add_one_callback))
    return job_queue


def start_bot():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    schedule_jobs(updater)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    start_bot()
