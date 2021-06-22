class AvitoHelper:

    def parse_housetype_to_avito_url(self, init_data):
        if init_data == "Новостройка":
            return "/novostroyka"
        if init_data == "Вторичка":
            return "/vtorichka"
        if init_data == "Не важно":
            return ""

    def parse_room_to_avito_url(self, init_data):
        if len(init_data) == 1:
            return init_data
        if len(init_data) == 3 or len(init_data) == 4:
            data = init_data.replace(',', '-').replace('-', ' ').split()
            return list(range(int(data[0]), int(data[1]) + 1))

    def parse_adtype_to_avito_url(self, init_data):
        if init_data == "Снимать":
            return "sdam"
        if init_data == "Купить":
            return "prodam"

    def parse_loc_to_avito_url(self, init_data):
        if init_data == "Пермь":
            return "perm"
        if init_data == "Добрянка":
            return "dobryanka"
        if init_data == "Пермский край":
            return "permskiy_kray"
        if init_data == "Лысьва":
            return "lysva"

    def get_path(self, users, id):
        location = self.parse_loc_to_avito_url(users[f'{id}']["city"])
        ad_type = self.parse_adtype_to_avito_url(users[f'{id}']["ad_type"])
        count_room = self.parse_room_to_avito_url(users[f'{id}']["count_room"])

        paths = []
        if ad_type == "sdam":
            if isinstance(count_room, list):
                for i in count_room:
                    paths.append(
                        f"avito/{location}/{ad_type}/{i}-komnatnye/")
            else:
                return f"avito/{location}/{ad_type}/{count_room}-komnatnye/"
        else:
            house_type = self.parse_housetype_to_avito_url(users[f'{id}']["house_type"])
            if isinstance(count_room, list):
                for i in count_room:
                    paths.append(
                        f"avito/{location}/{ad_type}{house_type}/{i}-komnatnye/")
            else:
                return f"avito/{location}/{ad_type}{house_type}/{count_room}-komnatnye/"
        return paths

    def get_url(self, users, id):

        location = self.parse_loc_to_avito_url(users[f'{id}']["city"])
        ad_type = self.parse_adtype_to_avito_url(users[f'{id}']["ad_type"])
        count_room = self.parse_room_to_avito_url(users[f'{id}']["count_room"])
        min_price = 0 if users[f'{id}']["min_price"] == "Нет" else users[f'{id}']["min_price"]
        max_price = 0 if users[f'{id}']["max_price"] == "Нет" else users[f'{id}']["max_price"]
        url = []
        if ad_type == "sdam":
            if isinstance(count_room, list):
                for i in count_room:
                    url.append(f"https://www.avito.ru/{location}/kvartiry/{ad_type}/{i}-komnatnye?pmax={max_price}&pmin={min_price}")
            else:
                return f"https://www.avito.ru/{location}/kvartiry/{ad_type}/{count_room}-komnatnye?pmax={max_price}&pmin={min_price}"
        else:
            house_type = self.parse_housetype_to_avito_url(users[f'{id}']["house_type"])
            if isinstance(count_room, list):
                for i in count_room:
                    url.append(f"https://www.avito.ru/{location}/kvartiry/{ad_type}/{i}-komnatnye{house_type}?pmax={max_price}&pmin={min_price}")
            else:
                return f"https://www.avito.ru/{location}/kvartiry/{ad_type}/{count_room}-komnatnye{house_type}?pmax={max_price}&pmin={min_price}"
        return url
