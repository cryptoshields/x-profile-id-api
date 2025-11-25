import re
from playwright.async_api import async_playwright

async def get_profile_id(username: str) -> str | None:
    username = username.removeprefix("@")
    url = f"https://x.com/{username}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            java_script_enabled=True,
        )
        # THESE TWO LINES ARE THE FIX
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")
        await context.add_cookies([{"name": "someCookie", "value": "1", "domain": ".x.com", "path": "/"}])

        page = await context.new_page()
        await page.goto(url, wait_until="networkidle", timeout=30000)

        content = await page.content()
        await browser.close()

        match = re.search(r'"userId":"(\d+)"', content)
        return match.group(1) if match else None
