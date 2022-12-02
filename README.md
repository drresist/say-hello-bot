# Say hello bot

- Simple script, that get weather from OW api, colleague birthdays from .csv file and after send that to TG chat
- Script run with cron job 

## Starting 

- Run docker image with next cmd docker run -e OW_API={openweather API token} -e TG_BOT_API={tg bot api} -e CHAT_ID={chat for sending} --rm       drresist/sh-bot:latest
