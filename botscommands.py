import asyncio
from loguru import logger
from math import ceil, floor

from origamibot import OrigamiBot
from origamibot.types import InputMediaPhoto

from getchapter import GetChapter
from exception import GetChapterFailed

class BotsCommands:
    def __init__(self, bot: OrigamiBot, data: dict) -> None:
        self.bot = bot
        self.data = data

    def get_chapter(self, message, value: str):
        logger.info("Trying get chapter "+value+" for "+message.from_user.username+"..")

        try:
            try: msg = asyncio.run(GetChapter(value, self.data["email_address"], self.data["password"]))
            except GetChapterFailed as e:
                logger.error("Failed to get chapter: "+str(e))
                self.bot.send_message(message.chat.id, str(e))
                return
            
            input_medias = []
                
            self.bot.send_message(message.chat.id, msg[0]+' - '+msg[1])
                
            for i, item in enumerate(msg[2]):
                input_medias.append(InputMediaPhoto(media=item,
                                                    caption=str(i+1),
                                                    parse_mode='html'))

            for_range = ceil(len(input_medias)/10) if len(input_medias)-floor(len(input_medias)/10)*10 != 1 else floor(len(input_medias)/10)
                
            for i in range(for_range):
                self.bot.send_media_group(message.chat.id, media=input_medias[i*10:(i+1)*10])
            
            if len(input_medias)-floor(len(input_medias)/10)*10 == 1:
                self.bot.send_photo(message.chat.id, input_medias[-1].media, input_medias[-1].caption)

            logger.info("Succesfully sended chapter "+value+" with "+str(len(input_medias))+" pages")
        except Exception as e:
            self.bot.send_message(message.chat.id, "Some issues with a bot..")
            logger.error("Failed to get chapter: "+str(e))