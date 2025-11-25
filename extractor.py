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
            locale="en-US",
            timezone_id="America/New_York",
        )
        page = await context.new_page()

        # Stealth script
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => false});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            window.chrome = { runtime: {} };
        """)

        # Fake cookie to simulate logged-out but real user
        await context.add_cookies([{"name": "auth_token", "value": "fake", "domain": ".x.com", "path": "/"}])

        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(5000)  # Wait for dynamic JS load

        content = await page.content()
        await browser.close()

        # More robust regex for userId in JSON or meta
        match = re.search(r'"userId"\s*:\s*"(\d+)"', content) or re.search(r'"rest_id"\s*:\s*"(\d+)"', content)
        return match.group(1) if match else None
