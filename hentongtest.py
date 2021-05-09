from Hentai import Hentai, Format, Utils
import asyncio

async def main():
    doujin = await Hentai.init(177013)
    print(doujin.url, doujin.title(Format.Pretty), doujin.image_urls, doujin.id)

asyncio.run(main())