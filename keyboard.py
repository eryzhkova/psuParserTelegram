from telebot import types

class TelegramKeyboards:

    def __init__(self, sites, city):
        self.sites = sites
        self.city = city

    def main_setting_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()

        realty_site = types.InlineKeyboardButton(text=f'Сайт объявлений [Выбрано: {self.sites}]', callback_data='sites')
        filters = types.InlineKeyboardButton(text='Критерии поиска', callback_data='filters')
        location = types.InlineKeyboardButton(text=f'Местоположение [{self.city}]', callback_data='location')
        confirmation = types.InlineKeyboardButton(text='Подтвердить', callback_data='confirmation')

        keyboard.add(realty_site)
        keyboard.add(filters)
        keyboard.add(location)
        keyboard.add(confirmation)
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
