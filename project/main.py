import asyncio
import browsers
from pyppeteer import launch

try:
    myBrowserPath = browsers.get("chrome")['path']
    print("Ścieżka: ", myBrowserPath)
except Exception as e:
    raise KeyError(f"Nie znaleziono {e}")

async def main():
    browserExecutablePath = myBrowserPath

    browser = await launch({
        'headless': False,
        'executablePath': browserExecutablePath,
    })

    page = await browser.newPage()

    await page.setViewport({'width': 800, 'height': 600})
    await page.goto('https://www.zieloneimperium.pl/login.php')
    await page.waitForSelector('#login_server')
    await page.select('#login_server', 'server1')
    await page.type('#login_user', 'login')
    await page.type('#login_pass', 'password')
    await page.click('#submitlogin')
    await page.waitForNavigation()

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
