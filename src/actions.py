import asyncio

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
