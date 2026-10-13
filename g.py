import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", headless=False)
        pg = await b.new_page()
        await pg.goto("https://sunnah.com/hisn", timeout=90000)
        await pg.wait_for_timeout(15000)
        open("hisn_full.html","w").write(await pg.content())
        await b.close()
asyncio.run(main())
