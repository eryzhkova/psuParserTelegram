import random
import time
import random
from selenium import webdriver
from fake_useragent import UserAgent

url = "https://www.avito.ru/perm"
useragent = UserAgent()
# options
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent.random}")

driver = webdriver.Chrome(
    executable_path="C:\\Users\\fryje\\PycharmProjects\\psuParserTelegram\\chromedriver.exe",
    options=options)

try:
    driver.get(url)
    time.sleep(5)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()