# extractor.py – FINAL WORKING VERSION FOR RAILWAY (Nov 2025)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, json, urllib.parse, random

def get_profile_id(username: str) -> str | None:
    username = username.strip().lstrip('@')
    url = f'https://x.com/{username}'

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # THIS IS THE CURRENT RAILWAY PATH (Nov 2025)
    options.binary_location = "/usr/bin/google-chrome"

    # Real UA rotation
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    ]
    options.add_argument(f'--user-agent={random.choice(uas)}')

    driver = webdriver.Chrome(options=options)

    # Ultimate stealth
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => false});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3]});
            window.chrome = { runtime: {},  };
        """
    })

    try:
        driver.get(url)
        time.sleep(9)  # X needs a second to load real content
        for entry in driver.get_log('performance'):
            message = json.loads(entry['message'])['message']
            if 'user_flow.json' in str(message):
                try:
                    data = message['params']['request']['postData']
                    payload = json.loads(urllib.parse.parse_qs(data)['log'][0])
                    for item in payload:
                        if isinstance(item, dict) and 'profile_id' in item:
                            return item['profile_id']
                except: continue
    except: pass
    finally:
        driver.quit()
    return None
