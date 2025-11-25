from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json, urllib.parse, time

def get_profile_id(username: str) -> str | None:
    username = username.strip().lstrip('@')
    url = f'https://x.com/{username}'

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')

    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
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
                    'user_flow.json' in msg['params']['request']['url'] and
                    'POST' in msg['params']['request']['method']):
                    data = msg['params']['request'].get('postData', '')
                    if 'log=' in data:
                        payload = json.loads(urllib.parse.parse_qs(data)['log'][0])
                        for item in payload:
                            if isinstance(item, dict) and 'profile_id' in item:
                                return item['profile_id']
            time.sleep(0.3)
    finally:
        driver.quit()
    return None