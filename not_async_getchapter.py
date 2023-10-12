import requests
from bs4 import BeautifulSoup

import json
from exception import GetChapterFailed
from utils import sanitize_text, ddir



def _GetChapter(response: requests.Response):
    ms = BeautifulSoup(response.text, "lxml")
    
    try: title = sanitize_text(ms.select_one(".series-header-title").text)
    except: raise GetChapterFailed("Chapter not found")
    chapter = sanitize_text(ms.select_one(".episode-header-title").text)

    prj = ms.select_one("script#episode-json")
    pd = ddir(json.loads(prj["data-value"]), "readableProduct/pageStructure/pages")
    pages = [i["src"] for i in pd if i["type"] == "main"]

    return title, chapter, pages


def GetChapter(num: str, email_address: str = None, password: str = None):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    link = "https://pocket.shonenmagazine.com"

    with requests.Session() as session:
        if email_address != None and password != None:
            data = {
                "email_address": email_address,
                "password": password
            }
            with session.post(url=link+"/user_account/login", data=data, headers=headers):
                with session.get(url=link+f"/episode/{num}", headers=headers) as response:
                    return _GetChapter(response)
        else:
            with session.get(url=link+f"/episode/{num}", headers=headers) as response:
                return _GetChapter(response)