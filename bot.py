import json

from auth_data import TOKEN
import telebot
from telebot import types
from keyboard import TelegramKeyboards


def telegram_keyboard(bot, user):
    # TODO: Сделать словари для критериев
    # TODO: Собрать ошибки для исключений

    count_sites = len(user["sites"])
    city = "Пермь"
    house_type = "Новостройка"
    ad_type = "Продажа"
    count_room = "1"
    min_price = "0"
    max_price = "2000000"

    settings_text = f'\n\n*Сайты*: {count_sites};\n*Типа дома*: {user["house_type"]};\n*Тип объявления*: {user["ad_type"]};\n*Количество комнат*: {user["count_room"]};\n*Цена*: от {user["min_price"]} до {user["max_price"]} руб.;\n*Местоположение*: {user["city"]}.'

    tel_keyboard = TelegramKeyboards(len(user["sites"]), user["city"])

    # Обработка команд
    @bot.message_handler(commands=["settings"])
    def start_message(message):
        bot.send_message(message.chat.id,
                         '*Настройка поиска* \nЗдесь ты можешь посмотреть настройки своего запроса '
                         'или изменить их',
                         reply_markup=tel_keyboard.main_setting_keyboard())

    @bot.message_handler(commands=["help"])
    def start_message(message):
        bot.send_message(message.chat.id, "Это бот для получений обновлений с сайтов объявлений Авито, Циан и "
                                          "Домофонд.\nЧтобы корректно работать следуй инструкциям в сообщениях и "
                                          "соблюдай шаблоны!")

    @bot.message_handler(commands=["stop"])
    def start_message(message):
        bot.send_message(message.chat.id, "Удаляем человека из БД")

    # Обработка callback'ов
    @bot.callback_query_handler(func=lambda call: call.data.startswith('settings'))
    def callback_settings(call):
        bot.send_message(call.message.chat.id,
                         '*Настройка поиска* \nЗдесь ты можешь посмотреть настройки своего запроса '
                         'или изменить их',
                         reply_markup=tel_keyboard.main_setting_keyboard())

    @bot.callback_query_handler(func=lambda call: call.data.startswith('sites'))
    def callback_sites(call):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='*Сайты объявлений* \nЗдесь ты можешь посмотреть свои настройки, '
                                   'связанные с _сайтами_, где искать объявления',
                              reply_markup=tel_keyboard.sites_setting_keyboard())

    # Обработка сайтов
    @bot.callback_query_handler(func=lambda call: call.data.startswith('avito'))
    def callback_sites_checked(call):
        sites = user["sites"]
        avito_checked = True
        cian_checked = False
        domofond_checked = False
        if "Авито" in sites:
            avito_checked = False
            sites.remove("Авито")
        else:
            sites.append("Авито")
        if "Циан" in sites:
            cian_checked = True
        if "Домофонд" in sites:
            domofond_checked = True
        user["sites"] = sites
        send_keyboard(avito_checked, cian_checked, domofond_checked, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('cian'))
    def callback_sites_checked(call):
        sites = user["sites"]
        avito_checked = False
        cian_checked = True
        domofond_checked = False
        if "Авито" in sites:
            avito_checked = True
        if "Циан" in sites:
            cian_checked = False
            sites.remove("Циан")
        else:
            sites.append("Циан")
        if "Домофонд" in sites:
            domofond_checked = True
        user["sites"] = sites
        send_keyboard(avito_checked, cian_checked, domofond_checked, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('domofond'))
    def callback_sites_checked(call):
        sites = user["sites"]
        avito_checked = False
        cian_checked = False
        domofond_checked = True
        if "Авито" in sites:
            avito_checked = True
        if "Циан" in sites:
            cian_checked = True
        if "Домофонд" in sites:
            domofond_checked = False
            sites.remove("Домофонд")
        else:
            sites.append("Домофонд")
        user["sites"] = sites
        send_keyboard(avito_checked, cian_checked, domofond_checked, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('delbtn'))
    def callback_sites_checked(call):
        user["sites"] = []
        send_keyboard(False, False, False, call)

    def send_keyboard(avito_checked, cian_checked, domofond_checked, call):
        text_avito = "Выбрано: " if avito_checked else ""
        text_cian = "Выбрано: " if cian_checked else ""
        text_domofond = "Выбрано: " if domofond_checked else ""
        keyboard = tel_keyboard.checked_sites_setting_keyboard(text_avito, text_cian, text_domofond)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('location'))
    def callback_location(call):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='*Местоположение* \nЗдесь ты можешь посмотреть свои настройки, '
                                   'связанные с _местоположением_, где искать объявления',
                              reply_markup=tel_keyboard.location_setting_keyboard())

    @bot.callback_query_handler(func=lambda call: call.data.startswith('okbtn'))
    def callback_ok(call):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='*Сайты объявлений* \nЗдесь ты можешь посмотреть настройки своего запроса '
                                   'или изменить их',
                              reply_markup=tel_keyboard.main_setting_keyboard())

    @bot.callback_query_handler(func=lambda call: call.data.startswith('view'))
    def callback_view(call):
        keyboard = types.InlineKeyboardMarkup()
        okbtn = types.InlineKeyboardButton(text='OK', callback_data='okbtn')
        keyboard.add(okbtn)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='*Настройки*' + settings_text,
                              reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('confirmation'))
    def callback_close(call):
        # TODO: сделать норм запись с проверкой наличия ID
        # new_settings = {f'{call.message.chat.id}: {user}'}
        with open("users.json", "w", encoding='utf-8') as file:
            json.dump(user, file, indent=4, ensure_ascii=False)
        bot.send_message(chat_id=call.message.chat.id,
                         text='*Все сохранено* \nИдет обработка запроса....')

    @bot.callback_query_handler(func=lambda call: call.data.startswith('filters'))
    def callback_filters(call):
        keyboard = types.InlineKeyboardMarkup()
        confirmation = types.InlineKeyboardButton(text='Подтвердить', callback_data='view')
        settings_btn = types.InlineKeyboardButton(text='Настроить', callback_data='filter_settings')
        keyboard.add(confirmation, settings_btn)
        if house_type is None and ad_type is None and count_room is None and min_price is None and max_price is None:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text='*Критерии поиска* \nУпс, у вас еще ничего не настроено!',
                                  reply_markup=keyboard)
        elif max_price == "Нет" and min_price == "Нет":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f'*Критерии поиска* \n\n*Типа дома*: {house_type};\n*Тип объявления*: {ad_type};\n*Количество комнат*: {count_room}.',
                                  reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f'*Критерии поиска* \n\n*Типа дома*: {house_type};\n*Тип объявления*: {ad_type};\n*Количество комнат*: {count_room};\n*Цена*: от {min_price} до {max_price} руб.',
                                  reply_markup=keyboard)

    # Обработка данных от пользователя
    @bot.callback_query_handler(func=lambda call: call.data.startswith('filter_settings'))
    def callback_filters_settings(call):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='*Критерии поиска* \nНастройка...', )
        house_chat(call.message)

    @bot.message_handler(content_types=["text"])
    def house_chat(message):
        msg = bot.send_message(chat_id=message.chat.id,
                               text='*Тип дома* \nКакой тип недвижимости Вас интересует?',
                               reply_markup=tel_keyboard.house_setting_replykeyboard())
        house_type = message.text
        print(house_type)
        bot.register_next_step_handler(msg, ad_chat)

    @bot.message_handler(content_types=["text"])
    def ad_chat(message):
        msg = bot.send_message(chat_id=message.chat.id,
                               text='*Тип объявления* \nХотите купить или снимать?',
                               reply_markup=tel_keyboard.ad_setting_replykeyboard())
        ad_type = message.text
        print(ad_type)
        bot.register_next_step_handler(msg, room_chat)

    @bot.message_handler(content_types=["text"])
    def room_chat(message):
        msg = bot.send_message(chat_id=message.chat.id,
                               text='*Количество комнат* \nКакое количество комнат? \nМожете выбрать из предложанных '
                                    'или ввести одну цифру, либо несколько через запятую (",") или дефис ("-").',
                               reply_markup=tel_keyboard.room_setting_replykeyboard())
        count_room = message.text
        print(count_room)
        if ad_type == "Снимать":
            bot.register_next_step_handler(msg, rent_min_chat)
        else:
            bot.register_next_step_handler(msg, sell_min_chat)

    @bot.message_handler(content_types=["text"])
    def rent_min_chat(message):
        msg = bot.send_message(chat_id=message.chat.id,
                               text='*Ограничения цены* \nВыберите или напишите минимальную цену недвижимости?',
                               reply_markup=tel_keyboard.rent_min_setting_replykeyboard())
        min_price = message.text
        print(min_price)
        bot.register_next_step_handler(msg, rent_max_chat)

    def rent_max_chat(message):
        msg = bot.send_message(chat_id=message.chat.id,
                               text='*Ограничения цены* \nВыберите или напишите максимальную цену недвижимости?',
                               reply_markup=tel_keyboard.rent_max_setting_replykeyboard())
        max_price = message.text
        print(max_price)
        bot.register_next_step_handler(msg, close_dialog)

    @bot.message_handler(content_types=["text"])
    def sell_min_chat(message):
        msg = bot.send_message(chat_id=message.chat.id,
                               text='*Ограничения цены* \nВыберите или напишите минимальную цену недвижимости?',
                               reply_markup=tel_keyboard.sell_min_setting_replykeyboard())
        min_price = message.text
        print(min_price)
        bot.register_next_step_handler(msg, sell_max_chat)

    @bot.message_handler(content_types=["text"])
    def sell_max_chat(message):
        msg = bot.send_message(chat_id=message.chat.id,
                               text='*Ограничения цены* \nВыберите или напишите максимальную цену недвижимости?',
                               reply_markup=tel_keyboard.sell_max_setting_replykeyboard())
        max_price = message.text
        print(max_price)
        bot.register_next_step_handler(msg, close_dialog)

    @bot.message_handler(content_types=["text"])
    def close_dialog(message):
        keyboard = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "Настройки сохранены.", reply_markup=keyboard)


def main():
    bot = telebot.TeleBot(TOKEN, parse_mode='Markdown')

    @bot.message_handler(commands=["start"])
    def start_message(message):
        keyboard = types.InlineKeyboardMarkup()
        settings_btn = types.InlineKeyboardButton(text='Настроить нужный поиск', callback_data='settings')
        keyboard.add(settings_btn)

        with open("users.json", encoding='utf-8') as file:
            users = json.load(file)
        try:
            user = users[f'{message.from_user.id}']
        except:
            user_settings = {
                "name": message.from_user.first_name,
                "sites": [],
                "city": None,
                "house_type": None,
                "ad_type": None,
                "count_room": None,
                "min_price": None,
                "max_price": None,
            }
            users[f'{message.from_user.id}'] = user_settings
            with open("users.json", "w", encoding='utf-8') as file:
                json.dump(users, file, indent=4, ensure_ascii=False)

        bot.send_message(message.chat.id,
                         f'*Привет, {message.from_user.first_name}!* \nНастрой бота с помощью кнопки и получай '
                         f'обновления! \nЕсли кнопка не отображается '
                         'напиши боту команду */settings*',
                         reply_markup=keyboard)
        telegram_keyboard(bot, users[f'{message.chat.id}'])

    bot.polling()


if __name__ == '__main__':
    main()
