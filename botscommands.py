from math import ceil

from origamibot import OrigamiBot
from origamibot.types import InputMediaPhoto

from not_async_getchapter import GetChapter
from exception import GetChapterFailed

class BotsCommands:
    def __init__(self, bot: OrigamiBot, data: dict) -> None:
        self.bot = bot
        self.data = data

    def get_chapter(self, message, value: str):
        print('Trying check chapter..')

        try: msg = GetChapter(value, self.data["email_address"], self.data["password"])
        except GetChapterFailed as e:
            self.bot.send_message(message.chat.id, str(e))
            return
        
        input_medias = []
            
        self.bot.send_message(message.chat.id, msg[0]+' - '+msg[1])
            
        for i, item in enumerate(msg[2]):
            input_medias.append(InputMediaPhoto(media=item,
                                                caption=str(i+1),
                                                parse_mode='html'))

        for i in range(ceil(len(msg[2])/10)):
            self.bot.send_media_group(message.chat.id, media=input_medias[i*10:(i+1)*10])

        print('Completed')