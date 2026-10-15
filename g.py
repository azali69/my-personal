import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", headless=False)
        pg = await b.new_page()
        await pg.goto("https://sunnah.com/shamail", timeout=90000)
        await pg.wait_for_timeout(15000)
        open("index.html","w").write(await pg.content())
        for c in range(1, 60):
            try:
                await pg.goto(f"https://sunnah.com/shamail/{c}", timeout=90000)
                await pg.wait_for_timeout(2500)
                html = await pg.content()
                open(f"ch{c}.html","w").write(html)
                print(c, len(html), flush=True)
            except Exception as e:
                print(c, 'ERR', e, flush=True)
        await b.close()
asyncio.run(main())
