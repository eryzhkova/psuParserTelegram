from site_helper import SiteHelper
from multiprocessing import Pool
import json
from bs4 import BeautifulSoup


class MockHelper:

    def __init__(self, id):
        self.id = id

    def parsing_data(self, path):
        with open(f"mock_data/htmls/{path}search.html", encoding='utf-8') as file:
            search = file.read()
        soup = BeautifulSoup(search, "lxml")

        if path.split('/')[0] == 'avito':
            items = soup.find_all('div', {'data-marker': 'item'})
            for item in items:
                url = item.find('a')['href']
                with open(f"mock_data/urls/{self.id}_urls.txt", "a", encoding='utf-8') as file:
                    file.write(url)
                    file.write('\n')
        if path.split('/')[0] == 'cian':
            items = soup.find_all('article', {'data-name': 'CardComponent'})
            for item in items:
                url = item.find('a')['href']
                with open(f"mock_data/urls/{self.id}_urls.txt", "a", encoding='utf-8') as file:
                    file.write(url)
                    file.write('\n')

        if path.split('/')[0] == 'domofond':
            pass

    def get_urls(self, users, id):
        urls = []
        sites = users[f'{id}']["sites"]
        site = SiteHelper()
        checked_sites = []

        if "Авито" in sites:
            checked_sites.append('avito')
        if "Циан" in sites:
            checked_sites.append('cian')
        if "Домофонд" in sites:
            checked_sites.append('domofond')

        for checked_site in checked_sites:
            if isinstance(site.get_path(users, id, checked_site), list):
                urls = urls + site.get_path(users, id, checked_site)
            else:
                urls.append(site.get_path(users, id, checked_site))

        return urls

    def get_data(self, id):
        with open("users.json", encoding='utf-8') as file:
            users = json.load(file)
        paths_list = self.get_urls(users, id)

        # очищаем файл
        with open(f"mock_data/urls/{self.id}_urls.txt", "w", encoding='utf-8'):
            pass

        proc = Pool(processes=len(paths_list))
        proc.map(self.parsing_data, paths_list)

        with open(f"mock_data/urls/{self.id}_urls.txt", encoding='utf-8') as file:
            urls_list = file.read()
            urls_list = urls_list.split()

        return urls_list
