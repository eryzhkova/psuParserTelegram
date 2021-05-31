from auth_data import CHROMEDRIVER_PATH, PROXY
from fake_useragent import UserAgent
from seleniumwire import webdriver
import requests
import json
import time

url = "https://www.vk.com/"

# options
user_agent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={user_agent.random}")

# set proxy
proxy_options = {
    "proxy": {
        "https": f"https://{PROXY}"
    }
}

driver = webdriver.Chrome(
    executable_path=CHROMEDRIVER_PATH,
    seleniumwire_options=proxy_options,
    options=options)

try:
    # driver.get("https://2ip.ru")
    # driver.get("https://www.whatismybrowser.com/detect/what-is-my-user-agent")
    driver.get(url)
    time.sleep(20)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()