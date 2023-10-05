from download import Downloader
import requests
from base import soup
from bs4 import BeautifulSoup

headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
            "X-Requested-With": "XMLHttpRequest"
          }

#url = "https://pocket.shonenmagazine.com/api/purchase/14079602755231591802"

Downloader(directory="C:\\Users\\Ybbb\\Desktop\\Manga").dlch("https://pocket.shonenmagazine.com/episode/14079602755231591802")

#session = requests.Session()
#session.post("https://pocket.shonenmagazine.com/user_account/login", headers=headers, data=data)

#response = session.post(url=url, headers=headers, data=data)

#ms = BeautifulSoup(response.text, "html.parser")

#print(ms)