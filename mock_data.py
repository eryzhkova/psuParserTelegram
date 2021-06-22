from avito_helper import AvitoHelper
from multiprocessing import Pool
import json
from bs4 import BeautifulSoup
import os


class MockHelper:

    def __init__(self, id):
        self.id = id

    def parsing_data(self, path):
        with open(f"mock_data/htmls/{path}search.html", encoding='utf-8') as file:
            search = file.read()
        soup = BeautifulSoup(search, "lxml")
        items = soup.find_all('div', {'data-marker': 'item'})
        for item in items:
            url = item.find('a')['href']
            with open(f"mock_data/urls/{self.id}_urls.txt", "a", encoding='utf-8') as file:
                file.write(url)
                file.write('\n')

    def get_urls(self, users, id):
        urls = []
        sites = users[f'{id}']["sites"]
        if "Авито" in sites:
            avito = AvitoHelper()
            if isinstance(avito.get_path(users, id), list):
                urls = urls + avito.get_path(users, id)
            else:
                urls.append(avito.get_path(users, id))
        if "Циан" in sites:
            urls.append("https://perm.cian.ru/")
        if "Домофонд" in sites:
            urls.append("https://www.domofond.ru/")

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

