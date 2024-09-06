from pyppeteer import launch
from browsers import get as get_browser

async def launch_browser(headless=False):
    try:
        my_browser_path = get_browser("chrome")['path']
        print("Ścieżka: ", my_browser_path)
    except Exception as e:
        raise KeyError(f"Nie znaleziono przeglądarki: {e}")

    browser = await launch({
        'headless': headless,
        'executablePath': my_browser_path,
        'args': [
            '--start-maximized',
        ]
    })
    page = await browser.newPage()

    screen_size = await page.evaluate('''() => {
            return {
                width: window.screen.availWidth,
                height: window.screen.availHeight
            };
        }''')

    await page.setViewport({
        'width': screen_size['width'],
        'height': screen_size['height']
    })

    return page

async def close_browser(browser):
    print("Naciśnij enter by zamknąć program...")
    input()
    await browser.close()
