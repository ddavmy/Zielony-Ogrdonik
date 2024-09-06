async def login(page, server, username, password):
    await page.goto('https://www.zieloneimperium.pl/login.php')
    await page.waitForSelector('#login_server')
    await page.select('#login_server', server)
    await page.type('#login_user', username)
    await page.type('#login_pass', password)
    await page.click('#submitlogin')
    await page.waitForNavigation()
