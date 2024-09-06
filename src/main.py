import asyncio
from src.utils import launch_browser, close_browser
from src.authorization import login
from src.actions import accept_cookies, harvest_crops, select_plant, water_unwatered_plants
from src.fieldAnalysis import get_gardenfields_with_image, get_gardenfields_without_watered_image


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

    # Określenie zajętych, pustych i niepodlanych pól uprawnych
    gardenfield_url = 'https://wurzelimperium.wavecdn.net/pics/'
    target_image_fragment = '0.gif'
    empty_space_background_image_url = f'{gardenfield_url}produkte/{target_image_fragment}'
    unwatered_plant_background_image_url = f'{gardenfield_url}{target_image_fragment}'

    empty_space_divs = await get_gardenfields_with_image(page, empty_space_background_image_url)

    unwatered_plants = await get_gardenfields_without_watered_image(page, unwatered_plant_background_image_url)

    # Wybór co chcemy uprawiać
    await select_plant("Marchewki", page)

    # Posadzenie w miejscu pustych pól uprawnych
    for div in empty_space_divs:
        await page.waitForSelector(f'#{div}')
        await page.evaluate(f'document.querySelector("#{div}").scrollIntoView();')
        await page.click(f'#{div}')

    # Podlanie niepodlanych pól uprawnych
    await water_unwatered_plants(page, unwatered_plants)

    # Zakończenie programu
    await close_browser(page)

if __name__ == "__main__":
    asyncio.run(main())
