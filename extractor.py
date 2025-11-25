import re
import asyncio
from playwright.async_api import async_playwright

async def get_profile_id(username: str) -> str | None:
    username = username.lstrip("@")
    url = f"https://x.com/{username}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")
        await page.goto(url, wait_until="networkidle", timeout=30000)

        # Grab profile_id from the page source (X embeds it in JSON)
        content = await page.content()
        match = re.search(r'"userId":"(\d+)"', content)
        if match:
            await browser.close()
            return match.group(1)

        await browser.close()
    return None
