import re
from playwright.async_api import async_playwright

async def get_profile_id(username: str) -> str | None:
    username = username.removeprefix("@")
    url = f"https://x.com/{username}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")
        await page.goto(url, wait_until="networkidle", timeout=30000)
        content = await page.content()
        await browser.close()

        match = re.search(r'"userId":"(\d+)"', content)
        return match.group(1) if match else None
