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

    # Określenie pustych pól uprawnych
    async def get_gardenfields_with_image(empty_url):
        divs_with_empty_background_image = await page.evaluate(f"""
            (backgroundImageUrl) => {{
                const gardenfields = Array.from(document.querySelectorAll('div.gardenfield'));
                const result = gardenfields.filter(div => {{
                    const childDivs = div.querySelectorAll('div');
                    return Array.from(childDivs).some(child => {{
                        const style = window.getComputedStyle(child);
                        return style.backgroundImage.includes(backgroundImageUrl);
                    }});
                }});
                return result.map(div => div.id);
            }}
        """, empty_url)

        return divs_with_empty_background_image

    # Określenie zajętych pól uprawnych
    async def get_gardenfields_with_different_image(target_image_fragment):
        divs_with_different_background_image = await page.evaluate(f"""
            (targetImageFragment) => {{
                const gardenfields = Array.from(document.querySelectorAll('div.gardenfield'));
                const result = gardenfields.filter(div => {{
                    const childDivs = div.querySelectorAll('div');
                    return Array.from(childDivs).some(child => {{
                        const style = window.getComputedStyle(child);
                        const backgroundImageUrl = style.backgroundImage;
                        const imageFragment = backgroundImageUrl.split('/produkte/')[1]?.replace('")', '');
                        return imageFragment && imageFragment !== targetImageFragment;
                    }});
                }});
                return result.map(div => div.id);
            }}
        """, target_image_fragment)

        return divs_with_different_background_image

    # Przekazanie danych do obliczenia ilości wolnych i zajętych pól
    target_image_fragment = '0.gif'
    empty_space_background_image_url = 'https://wurzelimperium.wavecdn.net/pics/produkte/0.gif'
    empty_space_divs = await get_gardenfields_with_image(empty_space_background_image_url)
    different_image_divs = await get_gardenfields_with_different_image(target_image_fragment)

    # Kliknięcie w puste pola uprawne
    for div in empty_space_divs:
        await page.waitForSelector(f'#{div}')
        await page.evaluate(f'document.querySelector("#{div}").scrollIntoView();')
        await page.click(f'#{div}')

    # Wyświetlenie liczby zajętych pól uprawnych
    not_empty_space_quantity = 0
    for div in different_image_divs:
        not_empty_space_quantity += 1
    print(not_empty_space_quantity)

    # Zakończenie programu
    print("Naciśnij enter by zamknąć pogram...")
    input()
    await browser.close()

asyncio.run(main())
