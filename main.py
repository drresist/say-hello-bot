# Import necessary libraries
import os
from typing import List
import requests
import time
import datetime
import telegram
from loguru import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, JobQueue
import json

# Set up weather API and Telegram API keys
weather_api_key: str = os.getenv("OW_API")
telegram_bot_token: str = os.getenv("TG_BOT_API")
chat_id: str = os.getenv("CHAT_ID")


counter: int = 0
pressed_users: dict = {}

def get_weather_data() -> str | None:
    """Get current weather data.

    Returns:
        str: Current weather data in string format.
        None: If failed to get weather data.
    """
    url: str = "http://api.openweathermap.org/data/2.5/weather"
    params: dict[str, str] = {
        "q": "Moscow",
        "appid": weather_api_key,
        "lang": "ru",
        "units": "metric"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        weather_data: dict = response.json()
        with open('icons.json', 'r', encoding='utf-8') as f:
            icons: dict = json.load(f)
        text: str = f"Погода {icons[weather_data['weather'][0]['icon']]}: {int(weather_data['main']['temp'])}°C" \
               f" (ощ. {int(weather_data['main']['feels_like'])}°C), " \
               f"{weather_data['weather'][0]['description']}"
        logger.info(text)
        return text
    except (requests.RequestException, json.JSONDecodeError):
        logger.exception("Failed to get weather data")
        return None

def send_weather_message(context: telegram.ext.CallbackContext) -> None:
    """Send weather message at 8 a.m. every day.

    Args:
        context (telegram.ext.CallbackContext): The context of the job.

    Returns:
        None
    """
    weather_data: str | None = get_weather_data()
    counter: int = 0
    keyboard: List[List[InlineKeyboardButton]] = [[InlineKeyboardButton("+1", callback_data="add_one")]]
    reply_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(keyboard)
    bot: telegram.Bot = telegram.Bot(token=telegram_bot_token)
    bot.send_message(chat_id=chat_id, text=weather_data, reply_markup=reply_markup)

def add_one_callback(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    """Callback function for +1 button.

    Args:
        update (telegram.Update): The received update.
        context (telegram.ext.CallbackContext): The context of the callback.

    Returns:
        None
    """
    global counter
    user_id = update.effective_user.id
    if user_id not in pressed_users:
        logger.info(f"Button pressed by user {update.effective_user.full_name} - {user_id}")
        counter += 1
        pressed_users[user_id] = True

def send_report_message(context: telegram.ext.CallbackContext) -> None:
    """Send report message at 9 a.m. every day.

    Args:
        context (telegram.ext.CallbackContext): The context of the job.

    Returns:
        None
    """
    global counter
    report_message: str = f"Проснулись: {counter} человек"
    bot: telegram.Bot = telegram.Bot(token=telegram_bot_token)
    bot.send_message(chat_id=chat_id, text=report_message)
    bot.edit_message_text(context.text, chat_id=chat_id, message_id=context.message.message_id)
    counter = 0
    pressed_users.clear()

updater: Updater = Updater(token=telegram_bot_token, use_context=True)
job_queue: JobQueue = updater.job_queue

job_queue.run_repeating(send_weather_message, interval=5)
updater.dispatcher.add_handler(CallbackQueryHandler(add_one_callback))

# Schedule report message to be sent at 9 a.m. every day
# job_queue.run_daily(send_report_message, time=datetime.time(hour=11, minute=54))
job_queue.run_repeating(send_report_message, interval=10)

# Start the bot
updater.start_polling()
updater.idle()