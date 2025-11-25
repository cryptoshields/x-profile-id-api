# extractor.py – FIXED for Railway's chromium/chromedriver (no binary_location needed)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time, json, urllib.parse, random, os

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
    options.add_argument('--disable-dev-tools')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-first-run')

    # UA rotation for stealth
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    ]
    options.add_argument(f'--user-agent={random.choice(uas)}')

    # Service for chromedriver (auto-found in PATH after nixpacks)
    service = Service()

    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => false});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3]});
                window.chrome = { runtime: {} };
            """
        })

        print(f"Loading {url}...")
        driver.get(url)
        start = time.time()
        while time.time() - start < 18:
            logs = driver.get_log('performance')
            for entry in logs:
                try:
                    msg = json.loads(entry['message'])['message']
                    if (msg['method'] == 'Network.requestWillBeSent' and
                        'user_flow.json' in msg['params']['request']['url'] and
                        msg['params']['request']['method'] == 'POST'):
                        post_data = msg['params']['request'].get('postData', '')
                        if 'log=' in post_data:
                            payload_str = urllib.parse.parse_qs(post_data)['log'][0]
                            payload = json.loads(payload_str)
                            for item in payload:
                                if isinstance(item, dict) and 'profile_id' in item:
                                    print(f"SUCCESS → Profile ID: {item['profile_id']}")
                                    return item['profile_id']
                except Exception as e:
                    print(f"Log parse error: {e}")
                    continue
            time.sleep(0.5)
        print("Timeout: No user_flow.json found")
    except Exception as e:
        print(f"Selenium error: {e}")
    finally:
        if driver:
            driver.quit()
    return None
