from utils.saucenao.saucenao_api import SauceNao

import asyncio

async def main():
    sauce = SauceNao('12ba41fbc533a3029c9c19b6d3d749cd76591402')
    results = await sauce.from_url('https://cdn.discordapp.com/attachments/623404074431283210/844110287309111336/unknown.png')

    print(results.long_remaining)
    print(results[1].title)
    print(results[1].urls)
    print(results[1].author)
    print(results[1].index_id)
    print(results[1].index_name)
    print(len(results))

asyncio.run(main())