import asyncio
import json
import os


async def click_if_present(page, selector, timeout=500):
    try:
        await page.waitForSelector(selector, visible=True, timeout=timeout)
        await page.click(selector)
    except asyncio.TimeoutError:
        print(f"Element {selector} nie został znaleziony przez {timeout}ms.")

async def accept_cookies(page):
    await page.waitForSelector('a.cookiemon-btn.cookiemon-btn-accept', timeout=500)
    await page.click('a.cookiemon-btn.cookiemon-btn-accept')
    await click_if_present(page, 'img.link.closeBtn')

async def harvest_crops(page):
    await page.waitForSelector('div[onclick="gardenjs.harvestAll()"]')
    await page.click('div[onclick="gardenjs.harvestAll()"]')

    await click_if_present(page, 'img.link.closeBtn')
    await click_if_present(page, '#baseDialogButton')

async def select_plant(name, page):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'data', 'products.json')

    with open(file_path, 'r') as f:
        data = json.load(f)

    data_class = data.get(name)
    await click_div_with_selected_plant(name, page, data_class)

async def click_div_with_selected_plant(name, page, number):
    selector = f'div#regal_{number}'
    try:
        await page.waitForSelector(selector, visible=True, timeout=500)
        await page.click(selector)
    except Exception as e:
        print(f"Na regale nie znaleziono {name}: {e}")


async def water_unwatered_plants(page, unwatered_plants):
    await page.waitForSelector('#giessen')
    await page.click('#giessen')

    for div in unwatered_plants:
        await page.waitForSelector(f'#{div}')
        await page.evaluate(f'document.querySelector("#{div}").scrollIntoView();')
        await page.click(f'#{div}')