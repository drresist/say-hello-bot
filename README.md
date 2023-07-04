# Telegram Weather Bot

This is a Telegram bot that provides current weather information for a specific location. It sends weather updates to a Telegram chat at 8 a.m. every day and allows users to increment a counter by pressing a +1 button. It also sends a report message at 9 a.m. every day.

## Getting Started

To use the Telegram Weather Bot, you'll need to perform the following steps:

1. Install the required libraries by running `pip install -r requirements.txt`.
2. Set up your environment variables:
   - `OW_API`: OpenWeatherMap API key for retrieving weather data.
   - `TG_BOT_API`: Telegram Bot API token for interacting with the Telegram bot.
   - `CHAT_ID`: Telegram chat ID where the bot will send messages.
3. Run the application by executing `python main.py`.

## Usage

Once the bot is running, it will automatically send weather updates at 8 a.m. every day to the specified Telegram chat. Users can press the +1 button to increment the counter, which will be included in the report message sent at 9 a.m. every day.

## Contributing

Contributions to this project are welcome. If you encounter any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).