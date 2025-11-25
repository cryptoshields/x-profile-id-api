from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json, urllib.parse, time

async def get_profile_id(username):
    # Clean up username: remove leading '@' if present
    username = username.strip().lstrip('@')
    
    url = f'https://x.com/{username}'

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')  # Windows UA for better stealth

    # THIS IS THE NEW WAY (2025) → loggingPrefs goes in options
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Hide webdriver flag
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined});'
    })

    try:
        print(f"Loading {url}...")
        driver.get(url)

        start = time.time()
        while time.time() - start < 15:
            logs = driver.get_log('performance')
            for entry in logs:
                try:
                    message = json.loads(entry['message'])['message']
                    if (message['method'] == 'Network.requestWillBeSent' and
                        'user_flow.json' in message['params']['request']['url'] and
                        message['params']['request']['method'] == 'POST'):

                        post_data = message['params']['request'].get('postData', '')
                        if 'log=' in post_data:
                            payload_str = urllib.parse.parse_qs(post_data)['log'][0]
                            payload = json.loads(payload_str)
                            for item in payload:
                                if isinstance(item, dict) and 'profile_id' in item:
                                    profile_id = item['profile_id']
                                    print(f"\nSUCCESS → Profile ID: {profile_id}")
                                    driver.quit()
                                    return profile_id
                except:
                    continue
            time.sleep(0.3)

        print("Timeout: No user_flow.json found")
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()
    return None
