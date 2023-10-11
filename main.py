import asyncio
from getchapter import GetChapter
from exception import GetChapterFailed

async def main():
    try:
        print(await GetChapter('14079602755231591802', data["email_address"], data["password"]))
    except GetChapterFailed as e:
        print(e)

asyncio.run(main())