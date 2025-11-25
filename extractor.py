import re
from playwright.async_api import async_playwright

async def get_profile_id(username: str) -> str | None:
    username = username.removeprefix("@")
    url = f"https://x.com/{username}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        )
        # tiny stealth
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")

        try:
            await page.goto(url, wait_until="networkidle", timeout=25000)
            content = await page.content()
            match = re.search(r'"userId":"(\d+)"', content)
            if match:
                return match.group(1)
        except:
            pass
        finally:
            await browser.close()
    return None
