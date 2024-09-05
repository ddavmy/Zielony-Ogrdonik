import asyncio
from browsers import get as get_browser
from pyppeteer import launch

try:
    myBrowserPath = get_browser("chrome")['path']
    print("Ścieżka: ", myBrowserPath)
except Exception as e:
    raise KeyError(f"Nie znaleziono {e}")

async def main():
    browser_executable_path = myBrowserPath

    browser = await launch({
        'headless': False,
        'executablePath': browser_executable_path,
    })

    page = await browser.newPage()

    # Logowanie
    await page.goto('https://www.zieloneimperium.pl/login.php')
    await page.waitForSelector('#login_server')
    await page.select('#login_server', 'server1')
    await page.type('#login_user', 'login')
    await page.type('#login_pass', 'password')
    await page.click('#submitlogin')
    await page.waitForNavigation()

    # Akceptacja Cookies
    await page.waitForSelector('a.cookiemon-btn.cookiemon-btn-accept', timeout=500)
    await page.click('a.cookiemon-btn.cookiemon-btn-accept')

    # Zebranie gotowych upraw
    await page.waitForSelector('div[onclick="gardenjs.harvestAll()"]')
    await page.click('div[onclick="gardenjs.harvestAll()"]')

    # Potwierdzenie komunikatu dotyczącego zebrania gotowych upraw
    try:
        await page.waitForSelector('img.link.closeBtn', visible=True, timeout=500)
        await page.click('img.link.closeBtn')
    except asyncio.TimeoutError:
        try:
            await page.waitForSelector('#baseDialogButton', visible=True, timeout=500)
            await page.evaluate('document.querySelector("#baseDialogButton").scrollIntoView();')
            await page.click('#baseDialogButton')
        except asyncio.TimeoutError:
            print("Nie znaleziono komunikatów zebrania upraw.")

    # Zakończenie programu
    print("Naciśnij enter by zamknąć pogram...")
    input()
    await browser.close()

asyncio.run(main())
