from site_helper import SiteHelper
from auth_data import CHROMEDRIVER_PATH, PROXY, TOKEN
from fake_useragent import UserAgent
from seleniumwire import webdriver
from multiprocessing import Pool
import json


class ParserHelper:

    def parsing_data(self, url):
        # options
        user_agent = UserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={user_agent.random}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")

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
            driver.get(url)
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    def get_urls(self, users, id):
        urls = []
        sites = users[f'{id}']["sites"]
        if "Авито" in sites:
            site = SiteHelper()
            if isinstance(site.get_url(users, id), list):
                urls = urls + site.get_url(users, id)
            else:
                urls.append(site.get_url(users, id))
        if "Циан" in sites:
            urls.append("https://perm.cian.ru/")
        if "Домофонд" in sites:
            urls.append("https://www.domofond.ru/")

        return urls

    def get_data(self, id):
        with open("users.json", encoding='utf-8') as file:
            users = json.load(file)
        urls_list = self.get_urls(users, id)
        print(urls_list)
        proc = Pool(processes=len(users[f'{id}']["sites"]))
        proc.map(self.parsing_data, urls_list)
