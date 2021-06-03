from auth_data import CHROMEDRIVER_PATH, PROXY
from fake_useragent import UserAgent
from seleniumwire import webdriver
import time


def main(url):
    # options
    user_agent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent.random}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")

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


if __name__ == '__main__':
    url = "https://www.vk.com/"
    main(url)
