from os import getenv
from time import sleep
from loguru import logger
from dotenv import load_dotenv
from origamibot import OrigamiBot
from botscommands import BotsCommands

# 14079602755231591802

if __name__ == '__main__':
    load_dotenv()
    data = {
        "email_address": getenv("EMAIL_ADDRESS"),
        "password": getenv("PASSWORD")
    }

    token = getenv("TOKEN")
    bot = OrigamiBot(token)

    bot.add_commands(BotsCommands(bot, data))

    bot.start()
    logger.info(bot.name+" is started")
    while True:
        sleep(1.5)