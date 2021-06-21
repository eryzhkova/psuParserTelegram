from telebot import types


class TelegramKeyboards:

    def main_setting_keyboard(self, users, id):
        keyboard = types.InlineKeyboardMarkup()
        sites = len(users[f'{id}']["sites"])
        city = users[f'{id}']["city"]

        realty_site = types.InlineKeyboardButton(text=f'Сайт объявлений [Выбрано: {sites}]', callback_data='sites')
        filters = types.InlineKeyboardButton(text='Критерии поиска', callback_data='filters')
        if city is None:
            location = types.InlineKeyboardButton(text='Местоположение [Не выбрано]', callback_data='location')
        else:
            location = types.InlineKeyboardButton(text=f'Местоположение [{city}]', callback_data='location')
        view = types.InlineKeyboardButton(text=f'Просмотр', callback_data='view')
        confirmation = types.InlineKeyboardButton(text='Подтвердить', callback_data='confirmation')

        keyboard.add(realty_site)
        keyboard.add(filters)
        keyboard.add(location)
        keyboard.add(view, confirmation)
        return keyboard

    def sites_setting_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()

        avito = types.InlineKeyboardButton(text=f'Авито', callback_data='avito')
        cian = types.InlineKeyboardButton(text='Циан', callback_data='cian')
        domofond = types.InlineKeyboardButton(text=f'Домофонд', callback_data='domofond')
        ok_btn = types.InlineKeyboardButton(text=f'ОК', callback_data='okbtn')

        keyboard.add(avito, cian, domofond)
        keyboard.add(ok_btn)
        return keyboard

    def checked_sites_setting_keyboard(self, text_avito, text_cian, text_domofond):
        keyboard = types.InlineKeyboardMarkup()
        avito = types.InlineKeyboardButton(text=f'{text_avito}Авито', callback_data='avito')
        cian = types.InlineKeyboardButton(text=f'{text_cian}Циан', callback_data='cian')
        domofond = types.InlineKeyboardButton(text=f'{text_domofond}Домофонд', callback_data='domofond')
        ok_btn = types.InlineKeyboardButton(text=f'ОК', callback_data='okbtn')
        del_btn = types.InlineKeyboardButton(text=f'Убрать все', callback_data='delbtn')

        keyboard.add(avito, cian, domofond)
        keyboard.add(ok_btn, del_btn)
        return keyboard

    def location_setting_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()

        perm = types.InlineKeyboardButton(text=f'Пермь', callback_data='perm')
        lisva = types.InlineKeyboardButton(text='Лысьва', callback_data='lysva')
        permkrai = types.InlineKeyboardButton(text=f'Пермский край', callback_data='permkrai')
        dobryanka = types.InlineKeyboardButton(text=f'Добрянка', callback_data='dobryanka')
        ok_btn = types.InlineKeyboardButton(text=f'ОК', callback_data='okbtn')

        keyboard.add(perm, lisva, dobryanka)
        keyboard.add(permkrai)
        keyboard.add(ok_btn)
        return keyboard

    def checked_location_setting_keyboard(self, text_perm, text_lysva, text_permkrai, text_dobryanka):
        keyboard = types.InlineKeyboardMarkup()
        perm = types.InlineKeyboardButton(text=f'{text_perm}Пермь', callback_data='perm')
        lisva = types.InlineKeyboardButton(text=f'{text_lysva}Лысьва', callback_data='lysva')
        permkrai = types.InlineKeyboardButton(text=f'{text_permkrai}Пермский край', callback_data='permkrai')
        dobryanka = types.InlineKeyboardButton(text=f'{text_dobryanka}Добрянка', callback_data='dobryanka')
        ok_btn = types.InlineKeyboardButton(text=f'ОК', callback_data='okbtn')
        del_btn = types.InlineKeyboardButton(text=f'Очистить', callback_data='clearbtn')

        keyboard.add(perm, lisva, dobryanka)
        keyboard.add(permkrai)
        keyboard.add(ok_btn, del_btn)
        return keyboard

    def house_setting_replykeyboard(self):
        keyboard = types.ReplyKeyboardMarkup()

        new_house = types.KeyboardButton(text='Новостройка')
        old_house = types.KeyboardButton(text='Вторичка')
        house = types.KeyboardButton(text='Не важно')

        keyboard.row(new_house, old_house)
        keyboard.row(house)
        return keyboard

    def ad_setting_replykeyboard(self):
        keyboard = types.ReplyKeyboardMarkup()

        sell_ad = types.KeyboardButton(text='Купить')
        rent_ad = types.KeyboardButton(text='Снимать')

        keyboard.row(sell_ad, rent_ad)
        return keyboard

    def room_setting_replykeyboard(self):
        keyboard = types.ReplyKeyboardMarkup()

        room = types.KeyboardButton(text='1')
        two = types.KeyboardButton(text='2')
        three = types.KeyboardButton(text='3')
        rooms13 = types.KeyboardButton(text='1-3')
        rooms12 = types.KeyboardButton(text='1-2')
        rooms23 = types.KeyboardButton(text='2-3')

        keyboard.row(room, two, three)
        keyboard.row(rooms13, rooms12, rooms23)
        return keyboard

    def rent_min_setting_replykeyboard(self):
        keyboard = types.ReplyKeyboardMarkup()
        min = types.KeyboardButton(text='Нет')
        min10 = types.KeyboardButton(text='10000')
        keyboard.row(min, min10)
        return keyboard

    def sell_min_setting_replykeyboard(self):
        keyboard = types.ReplyKeyboardMarkup()

        min = types.KeyboardButton(text='Нет')
        min1 = types.KeyboardButton(text='1000000')

        keyboard.row(min, min1)
        return keyboard

    def rent_max_setting_replykeyboard(self):
        keyboard = types.ReplyKeyboardMarkup()

        no_max = types.KeyboardButton(text='Нет')
        max20 = types.KeyboardButton(text='20000')

        keyboard.row(no_max, max20)
        return keyboard

    def sell_max_setting_replykeyboard(self):
        keyboard = types.ReplyKeyboardMarkup()

        no_max = types.KeyboardButton(text='Нет')
        max20 = types.KeyboardButton(text='2000000')

        keyboard.row(no_max, max20)
        return keyboard
