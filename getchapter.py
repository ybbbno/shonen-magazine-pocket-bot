import aiohttp
from bs4 import BeautifulSoup

import json
from exception import GetChapterFailed
from utils import sanitize_text, ddir

    
async def _GetChapter(response: aiohttp.client_reqrep.ClientResponse):
    text = await response.read()
    ms = BeautifulSoup(text.decode("utf-8"), "lxml")
    
    try: title = sanitize_text(ms.select_one(".series-header-title").text)
    except: raise GetChapterFailed("Chapter not found")
    chapter = sanitize_text(ms.select_one(".episode-header-title").text)

    prj = ms.select_one("script#episode-json")
    pd = ddir(json.loads(prj["data-value"]), "readableProduct/pageStructure/pages")
    pages = [i["src"] for i in pd if i["type"] == "main"]

    return title, chapter, pages

async def GetChapter(num: str, email_address: str = None, password: str = None):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest"
    }
        
    async with aiohttp.ClientSession("https://pocket.shonenmagazine.com") as session:
        if email_address != None and password != None:
            data = {
                "email_address": email_address,
                "password": password
            }
            async with session.post(url="/user_account/login", data=data, headers=headers):
                async with session.get(url=f"/episode/{num}", headers=headers) as response:
                    return await _GetChapter(response)
        else:
            async with session.get(url=f"/episode/{num}", headers=headers) as response:
                return await _GetChapter(response)