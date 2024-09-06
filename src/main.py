import asyncio
from src.utils import launch_browser, close_browser
from src.authorization import login
from src.actions import accept_cookies, harvest_crops
from src.fieldAnalysis import get_gardenfields_with_image, get_gardenfields_with_different_image

async def main():
    # Włączenie przeglądarki
    page = await launch_browser(headless=False)

    # Logowanie
    server = 'server1'
    username = 'login'
    password = 'password'
    await login(page, server, username, password)

    # Akceptacja ciasteczek i zebranie gotowych upraw
    await accept_cookies(page)
    await harvest_crops(page)

    # Określenie zajętych i pustych pól uprawnych
    empty_space_background_image_url = 'https://wurzelimperium.wavecdn.net/pics/produkte/0.gif'
    target_image_fragment = '0.gif'

    empty_space_divs = await get_gardenfields_with_image(page, empty_space_background_image_url)
    different_image_divs = await get_gardenfields_with_different_image(page, target_image_fragment)

    # Posadzenie w miejscu pustych pól uprawnych
    for div in empty_space_divs:
        await page.waitForSelector(f'#{div}')
        await page.evaluate(f'document.querySelector("#{div}").scrollIntoView();')
        await page.click(f'#{div}')

    # Wyświetlenie liczby zajętych pól uprawnych
    not_empty_space_quantity = len(different_image_divs)
    print(f"Number of occupied fields: {not_empty_space_quantity}")

    # Zakończenie programu
    await close_browser(page)

if __name__ == "__main__":
    asyncio.run(main())
