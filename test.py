import asyncio
import aiohttp
from bs4 import BeautifulSoup
from async_class import AsyncClass

class PSM(AsyncClass):
    async def __ainit__(self, email_address: str = None, password: str = None) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
            "X-Requested-With": "XMLHttpRequest"
        }

        if email_address != None and password != None:
            self.data = {
                "email_address": email_address,
                "password": password
            }
        else: self.data = None

    async def _get_session(self) -> (aiohttp._RequestContextManager | aiohttp.ClientSession):
        session = aiohttp.ClientSession("https://pocket.shonenmagazine.com")
        if self.data != None:
            session = session.post(url="/user_account/login",
                                   data=self.data,
                                   headers=self.headers)
        return session

    async def find_series(self, name: str) -> list:
        '''
        а
        '''
        session = await self._get_session()

        async with session.get(url="/search",
                               headers=self.headers,
                               params={'q': name}) as response:

            text = await response.read()
            ms = BeautifulSoup(text.decode("utf-8"), "lxml")

            series = []
            for obj in ms.find('ul', class_='series-list').find_all('li'):
                series.append({
                    'title': obj.find('p', class_='series-title').text,
                    'author': obj.find('p', class_='author').text,
                    'image': obj.find('img').get('src'),
                    'first_chapter': obj.find('a', class_='main-link').get('href'),
                    'last_chapter': obj.find('a', class_='sub-link').get('href') if obj.find('a', class_='sub-link') != None else None
                    })

            await session.close()
            return series

async def main():
    psm = await PSM()
    series = await psm.find_series('十字架のろくにん')

if __name__ == '__main__':
    asyncio.run(main())