# extractor.py – Railway-fixed version (Nov 2025)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
import os
import time
import json
import urllib.parse

def get_profile_id(username: str) -> str | None:
    username = username.strip().lstrip('@')
    url = f'https://x.com/{username}'

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')
    options.add_argument('--disable-javascript')  # optional speed-up
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    # Critical Railway fixes
    options.add_argument('--remote-debugging-port=9222')
    options.binary_location = "/usr/bin/chromium-browser"  # Railway's chromium path

    try:
        driver = webdriver.Chrome(options=options)  # No service → uses system chromedriver
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined});'
        })

        driver.get(url)
        start = time.time()
        while time.time() - start < 18:
            logs = driver.get_log('performance')
            for entry in logs:
                msg = json.loads(entry['message'])['message']
                if (msg['method'] == 'Network.requestWillBeSent' and
                    'user_flow.json' in msg['params']['request']['url']):
                    data = msg['params']['request'].get('postData', '')
                    if 'log=' in data:
                        payload = json.loads(urllib.parse.parse_qs(data)['log'][0])
                        for item in payload:
                            if isinstance(item, dict) and 'profile_id' in item:
                                return item['profile_id']
            time.sleep(0.3)
    except Exception as e:
        print("Selenium error:", e)
        return None
    finally:
        try:
            driver.quit()
        except:
            pass
    return None
