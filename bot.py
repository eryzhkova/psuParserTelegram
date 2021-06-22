import json

from auth_data import TOKEN
import telebot
from telebot import types
from keyboard import TelegramKeyboards
from mock_data import MockHelper


# from parser_helper import ParserHelper

def telegram_keyboard(bot, users):
    # TODO: Сделать словари для критериев
    # TODO: Собрать ошибки для исключений

    tel_keyboard = TelegramKeyboards()

    # Обработка команд
    @bot.message_handler(commands=["settings"])
    def start_message(message):
        bot.send_message(message.chat.id,
                         '*Настройка поиска* \nЗдесь ты можешь посмотреть настройки своего запроса '
                         'или изменить их',
                         reply_markup=tel_keyboard.main_setting_keyboard(users, message.chat.id))

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
                         reply_markup=tel_keyboard.main_setting_keyboard(users, call.message.chat.id))

    @bot.callback_query_handler(func=lambda call: call.data.startswith('okbtn'))
    def callback_ok(call):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='*Сайты объявлений* \nЗдесь ты можешь посмотреть настройки своего запроса '
                                   'или изменить их',
                              reply_markup=tel_keyboard.main_setting_keyboard(users, call.message.chat.id))

    @bot.callback_query_handler(func=lambda call: call.data.startswith('view'))
    def callback_view(call):
        keyboard = types.InlineKeyboardMarkup()
        okbtn = types.InlineKeyboardButton(text='OK', callback_data='okbtn')
        keyboard.add(okbtn)
        if users[f"{call.message.chat.id}"]["house_type"] is None and users[f"{call.message.chat.id}"][
            "ad_type"] is None and users[f"{call.message.chat.id}"]["count_room"] is None and \
                users[f"{call.message.chat.id}"]["min_price"] is None and users[f"{call.message.chat.id}"][
            "max_price"] is None:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text='*Настройки* \nУпс, у вас еще ничего не настроено!',
                                  reply_markup=keyboard)
        elif users[f"{call.message.chat.id}"]["min_price"] == "Нет" and users[f"{call.message.chat.id}"][
            "max_price"] == "Нет":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f'*Настройки* \n\n*Сайты*: {users[f"{call.message.chat.id}"]["sites"]};\n*Тип дома*: {users[f"{call.message.chat.id}"]["house_type"]};\n*Тип объявления*: {users[f"{call.message.chat.id}"]["ad_type"]};\n*Количество комнат*: {users[f"{call.message.chat.id}"]["count_room"]};\n*Местоположение*: {users[f"{call.message.chat.id}"]["city"]}.\n',
                                  reply_markup=keyboard)
        elif users[f"{call.message.chat.id}"]["min_price"] == "Нет" and users[f"{call.message.chat.id}"][
            "max_price"] != "Нет":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f'*Настройки* \n\n*Сайты*: {users[f"{call.message.chat.id}"]["sites"]};\n*Тип дома*: {users[f"{call.message.chat.id}"]["house_type"]};\n*Тип объявления*: {users[f"{call.message.chat.id}"]["ad_type"]};\n*Количество комнат*: {users[f"{call.message.chat.id}"]["count_room"]};\n*Цена*: до {users[f"{call.message.chat.id}"]["max_price"]} руб.;\n*Местоположение*: {users[f"{call.message.chat.id}"]["city"]}.\n',
                                  reply_markup=keyboard)
        elif users[f"{call.message.chat.id}"]["min_price"] != "Нет" and users[f"{call.message.chat.id}"][
            "max_price"] == "Нет":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f'*Настройки* \n\n*Сайты*: {users[f"{call.message.chat.id}"]["sites"]};\n*Тип дома*: {users[f"{call.message.chat.id}"]["house_type"]};\n*Тип объявления*: {users[f"{call.message.chat.id}"]["ad_type"]};\n*Количество комнат*: {users[f"{call.message.chat.id}"]["count_room"]};\n*Цена*: от {users[f"{call.message.chat.id}"]["min_price"]} руб.;\n*Местоположение*: {users[f"{call.message.chat.id}"]["city"]}.\n',
                                  reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f'*Настройки* \n\n*Сайты*: {users[f"{call.message.chat.id}"]["sites"]};\n*Тип дома*: {users[f"{call.message.chat.id}"]["house_type"]};\n*Тип объявления*: {users[f"{call.message.chat.id}"]["ad_type"]};\n*Количество комнат*: {users[f"{call.message.chat.id}"]["count_room"]};\n*Цена*: от {users[f"{call.message.chat.id}"]["min_price"]} до {users[f"{call.message.chat.id}"]["max_price"]} руб.;\n*Местоположение*: {users[f"{call.message.chat.id}"]["city"]}.\n',
                                  reply_markup=keyboard)

    item_count = 0
    data_list = []

    @bot.callback_query_handler(func=lambda call: call.data.startswith('confirmation'))
    def callback_close(call):
        user_settings = {
            "name": call.message.from_user.first_name,
            "sites": users[f'{call.message.chat.id}']["sites"],
            "city": users[f'{call.message.chat.id}']["city"],
            "house_type": users[f'{call.message.chat.id}']["house_type"],
            "ad_type": users[f'{call.message.chat.id}']["ad_type"],
            "count_room": users[f'{call.message.chat.id}']["count_room"],
            "min_price": users[f'{call.message.chat.id}']["min_price"],
            "max_price": users[f'{call.message.chat.id}']["max_price"],
        }
        users[f'{call.message.chat.id}'] = user_settings
        with open("users.json", "w", encoding='utf-8') as file:
            json.dump(users, file, indent=4, ensure_ascii=False)
        bot.send_message(chat_id=call.message.chat.id,
                         text='*Все сохранено* \nИдет обработка запроса....')
        # Для реальных запросов
        # parser_helper = ParserHelper()
        # parser_helper.get_data(call.message.chat.id)

        # Для мокс-запросов
        mock_data = MockHelper(call.message.chat.id)
        nonlocal data_list
        data_list = mock_data.get_data(call.message.chat.id)
        send_response_data(call)

    def send_response_data(call):
        keyboard = types.InlineKeyboardMarkup()

        next = types.InlineKeyboardButton(text='Далее', callback_data='next')
        main = types.InlineKeyboardButton(text='В главное меню', callback_data='main')
        keyboard.add(next, main)

        nonlocal data_list
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='*Все сохранено* \nСейчас Вам будут приходить ссылки на объекты, которые '
                                   'соответствуют вашему запросу по одному.\n\n'
                                   'Чтобы получить следующий объект - нажмите "Далее"\n'
                                   'Чтобы выйти в главное меню и изменить настройки '
                                   'и перестать получать обновление - нажмите "В главное меню"')
        text = f'[{data_list[0]}]({data_list[0]})'
        bot.send_message(chat_id=call.message.chat.id,
                             text=f'*Ссылка по запросу* \n{text}',
                             reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('next'))
    def callback_next(call):
        keyboard = types.InlineKeyboardMarkup()

        next = types.InlineKeyboardButton(text='Далее', callback_data='next')
        main = types.InlineKeyboardButton(text='В главное меню', callback_data='main')
        keyboard.add(next, main)

        nonlocal item_count
        nonlocal data_list

        item_count += 1
        print(item_count)
        text = f'[{data_list[item_count]}]({data_list[item_count]})'
        bot.send_message(chat_id=call.message.chat.id,
                         text=f'*Ссылка по запросу* \n{text}',
                         reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('main'))
    def callback_main(call):
        bot.send_message(chat_id=call.message.chat.id,
                         text='*Сайты объявлений* \nЗдесь ты можешь посмотреть настройки своего запроса '
                              'или изменить их',
                         reply_markup=tel_keyboard.main_setting_keyboard(users, call.message.chat.id))

    # Обработка сайтов
    @bot.callback_query_handler(func=lambda call: call.data.startswith('sites'))
    def callback_sites(call):
        if len(users[f'{call.message.chat.id}']["sites"]) == 0:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text='*Сайты объявлений* \nЗдесь ты можешь посмотреть свои настройки, '
                                       'связанные с _сайтами_, где искать объявления',
                                  reply_markup=tel_keyboard.sites_setting_keyboard())
        else:
            if "Авито" in users[f'{call.message.chat.id}']["sites"]:
                avito_checked = True
            else:
                avito_checked = False
            if "Циан" in users[f'{call.message.chat.id}']["sites"]:
                cian_checked = True
            else:
                cian_checked = False
            if "Домофонд" in users[f'{call.message.chat.id}']["sites"]:
                domofond_checked = True
            else:
                domofond_checked = False
            send_keyboard(avito_checked, cian_checked, domofond_checked, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('avito'))
    def callback_sites_checked(call):
        if "Авито" in users[f'{call.message.chat.id}']["sites"]:
            avito_checked = False
            users[f'{call.message.chat.id}']["sites"].remove("Авито")
        else:
            avito_checked = True
            users[f'{call.message.chat.id}']["sites"].append("Авито")
        if "Циан" in users[f'{call.message.chat.id}']["sites"]:
            cian_checked = True
        else:
            cian_checked = False
        if "Домофонд" in users[f'{call.message.chat.id}']["sites"]:
            domofond_checked = True
        else:
            domofond_checked = False
        send_keyboard(avito_checked, cian_checked, domofond_checked, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('cian'))
    def callback_sites_checked(call):
        if "Авито" in users[f'{call.message.chat.id}']["sites"]:
            avito_checked = True
        else:
            avito_checked = False
        if "Циан" in users[f'{call.message.chat.id}']["sites"]:
            cian_checked = False
            users[f'{call.message.chat.id}']["sites"].remove("Циан")
        else:
            cian_checked = True
            users[f'{call.message.chat.id}']["sites"].append("Циан")
        if "Домофонд" in users[f'{call.message.chat.id}']["sites"]:
            domofond_checked = True
        else:
            domofond_checked = False
        send_keyboard(avito_checked, cian_checked, domofond_checked, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('domofond'))
    def callback_sites_checked(call):
        if "Авито" in users[f'{call.message.chat.id}']["sites"]:
            avito_checked = True
        else:
            avito_checked = False
        if "Циан" in users[f'{call.message.chat.id}']["sites"]:
            cian_checked = True
        else:
            cian_checked = False
        if "Домофонд" in users[f'{call.message.chat.id}']["sites"]:
            domofond_checked = False
            users[f'{call.message.chat.id}']["sites"].remove("Домофонд")
        else:
            domofond_checked = True
            users[f'{call.message.chat.id}']["sites"].append("Домофонд")
        send_keyboard(avito_checked, cian_checked, domofond_checked, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('delbtn'))
    def callback_sites_checked(call):
        users[f'{call.message.chat.id}']["sites"] = []
        send_keyboard(False, False, False, call)

    def send_keyboard(avito_checked, cian_checked, domofond_checked, call):
        text_avito = "Выбрано: " if avito_checked else ""
        text_cian = "Выбрано: " if cian_checked else ""
        text_domofond = "Выбрано: " if domofond_checked else ""
        keyboard = tel_keyboard.checked_sites_setting_keyboard(text_avito, text_cian, text_domofond)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=keyboard)

    # Обработка местоположения
    @bot.callback_query_handler(func=lambda call: call.data.startswith('location'))
    def callback_location(call):
        if users[f'{call.message.chat.id}']["city"] is None:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text='*Местоположение* \nЗдесь ты можешь посмотреть свои настройки, '
                                       'связанные с _местоположением_, где искать объявления',
                                  reply_markup=tel_keyboard.location_setting_keyboard())
        else:
            if users[f'{call.message.chat.id}']["city"] == "Пермь":
                perm_checked = True
                lysva_checked = False
                permkrai_checked = False
                dobryanka_checked = False
            else:
                perm_checked = False
                if users[f'{call.message.chat.id}']["city"] == "Лысьва":
                    lysva_checked = True
                    permkrai_checked = False
                    dobryanka_checked = False
                else:
                    lysva_checked = False
                    if users[f'{call.message.chat.id}']["city"] == "Пермский край":
                        permkrai_checked = True
                        dobryanka_checked = False
                    else:
                        permkrai_checked = False
                        if users[f'{call.message.chat.id}']["city"] == "Добрянка":
                            dobryanka_checked = True
                        else:
                            dobryanka_checked = False
            send_loc_keyboard(perm_checked, lysva_checked, permkrai_checked, dobryanka_checked, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('perm'))
    def callback_perm_checked(call):
        if users[f'{call.message.chat.id}']["city"] == "Пермь":
            perm_checked = False
            lysva_checked = False
            permkrai_checked = False
            dobryanka_checked = False
            users[f'{call.message.chat.id}']["city"] = []
        else:
            perm_checked = True
            users[f'{call.message.chat.id}']["city"] = "Пермь"
            lysva_checked = False
            permkrai_checked = False
            dobryanka_checked = False
        send_loc_keyboard(perm_checked, lysva_checked, permkrai_checked, dobryanka_checked, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('lysva'))
    def callback_perm_checked(call):
        if users[f'{call.message.chat.id}']["city"] == "Лысьва":
            perm_checked = False
            lysva_checked = False
            permkrai_checked = False
            dobryanka_checked = False
            users[f'{call.message.chat.id}']["city"] = []
        else:
            perm_checked = False
            lysva_checked = True
            permkrai_checked = False
            dobryanka_checked = False
            users[f'{call.message.chat.id}']["city"] = "Лысьва"
        send_loc_keyboard(perm_checked, lysva_checked, permkrai_checked, dobryanka_checked, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('permkrai'))
    def callback_perm_checked(call):
        if users[f'{call.message.chat.id}']["city"] == "Пермский край":
            perm_checked = False
            lysva_checked = False
            permkrai_checked = False
            dobryanka_checked = False
            users[f'{call.message.chat.id}']["city"] = []
        else:
            perm_checked = False
            lysva_checked = False
            permkrai_checked = True
            dobryanka_checked = False
            users[f'{call.message.chat.id}']["city"] = "Пермский край"
        send_loc_keyboard(perm_checked, lysva_checked, permkrai_checked, dobryanka_checked, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('dobryanka'))
    def callback_perm_checked(call):
        if users[f'{call.message.chat.id}']["city"] == "Добрянка":
            perm_checked = False
            lysva_checked = False
            permkrai_checked = False
            dobryanka_checked = False
            users[f'{call.message.chat.id}']["city"] = []
        else:
            perm_checked = False
            lysva_checked = False
            permkrai_checked = False
            dobryanka_checked = True
            users[f'{call.message.chat.id}']["city"] = "Добрянка"
        send_loc_keyboard(perm_checked, lysva_checked, permkrai_checked, dobryanka_checked, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('clearbtn'))
    def callback_location_checked(call):
        users[f'{call.message.chat.id}']["city"] = []
        send_loc_keyboard(False, False, False, False, call)

    def send_loc_keyboard(perm_checked, lysva_checked, permkrai_checked, dobryanka_checked, call):
        text_perm = "Выбрано: " if perm_checked else ""
        text_lysva = "Выбрано: " if lysva_checked else ""
        text_permkrai = "Выбрано: " if permkrai_checked else ""
        text_dobryanka = "Выбрано: " if dobryanka_checked else ""
        keyboard = tel_keyboard.checked_location_setting_keyboard(text_perm, text_lysva, text_permkrai, text_dobryanka)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=keyboard)

    # Обработка критериев поиска
    @bot.callback_query_handler(func=lambda call: call.data.startswith('filters'))
    def callback_filters(call):
        keyboard = types.InlineKeyboardMarkup()
        okbtn = types.InlineKeyboardButton(text='OK', callback_data='okbtn')
        settings_btn = types.InlineKeyboardButton(text='Настроить', callback_data='filter_settings')
        keyboard.add(okbtn, settings_btn)
        if users[f"{call.message.chat.id}"]["house_type"] is None and users[f"{call.message.chat.id}"][
            "ad_type"] is None and users[f"{call.message.chat.id}"]["count_room"] is None and \
                users[f"{call.message.chat.id}"]["min_price"] is None and users[f"{call.message.chat.id}"][
            "max_price"] is None:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text='*Критерии поиска* \nУпс, у вас еще ничего не настроено!',
                                  reply_markup=keyboard)
        elif users[f"{call.message.chat.id}"]["min_price"] == "Нет" and users[f"{call.message.chat.id}"][
            "max_price"] == "Нет":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f'*Критерии поиска* \n\n*Типа дома*: {users[f"{call.message.chat.id}"]["house_type"]};\n*Тип объявления*: {users[f"{call.message.chat.id}"]["ad_type"]};\n*Количество комнат*: {users[f"{call.message.chat.id}"]["count_room"]}.',
                                  reply_markup=keyboard)
        elif users[f"{call.message.chat.id}"]["min_price"] == "Нет" and users[f"{call.message.chat.id}"][
            "max_price"] != "Нет":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f'*Критерии поиска* \n\n*Типа дома*: {users[f"{call.message.chat.id}"]["house_type"]};\n*Тип объявления*: {users[f"{call.message.chat.id}"]["ad_type"]};\n*Количество комнат*: {users[f"{call.message.chat.id}"]["count_room"]};\n*Цена*: до {users[f"{call.message.chat.id}"]["max_price"]} руб.',
                                  reply_markup=keyboard)
        elif users[f"{call.message.chat.id}"]["min_price"] != "Нет" and users[f"{call.message.chat.id}"][
            "max_price"] == "Нет":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f'*Критерии поиска* \n\n*Типа дома*: {users[f"{call.message.chat.id}"]["house_type"]};\n*Тип объявления*: {users[f"{call.message.chat.id}"]["ad_type"]};\n*Количество комнат*: {users[f"{call.message.chat.id}"]["count_room"]};\n*Цена*: от {users[f"{call.message.chat.id}"]["min_price"]} руб.',
                                  reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f'*Критерии поиска* \n\n*Типа дома*: {users[f"{call.message.chat.id}"]["house_type"]};\n*Тип объявления*: {users[f"{call.message.chat.id}"]["ad_type"]};\n*Количество комнат*: {users[f"{call.message.chat.id}"]["count_room"]};\n*Цена*: от {users[f"{call.message.chat.id}"]["min_price"]} до {users[f"{call.message.chat.id}"]["max_price"]} руб.',
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
        bot.register_next_step_handler(msg, ad_chat)

    @bot.message_handler(content_types=["text"])
    def ad_chat(message):
        house_type = message.text
        users[f'{message.chat.id}']["house_type"] = house_type
        msg = bot.send_message(chat_id=message.chat.id,
                               text='*Тип объявления* \nХотите купить или снимать?',
                               reply_markup=tel_keyboard.ad_setting_replykeyboard())
        bot.register_next_step_handler(msg, room_chat)

    @bot.message_handler(content_types=["text"])
    def room_chat(message):
        ad_type = message.text
        users[f'{message.chat.id}']["ad_type"] = ad_type
        msg = bot.send_message(chat_id=message.chat.id,
                               text='*Количество комнат* \nКакое количество комнат? \nМожете выбрать из предложанных '
                                    'или ввести одну цифру, либо несколько через запятую (",") или дефис ("-").',
                               reply_markup=tel_keyboard.room_setting_replykeyboard())
        if ad_type == "Снимать":
            bot.register_next_step_handler(msg, rent_min_chat)
        else:
            bot.register_next_step_handler(msg, sell_min_chat)

    @bot.message_handler(content_types=["text"])
    def rent_min_chat(message):
        count_room = message.text
        users[f'{message.chat.id}']["count_room"] = count_room
        msg = bot.send_message(chat_id=message.chat.id,
                               text='*Ограничения цены* \nВыберите или напишите минимальную цену недвижимости?',
                               reply_markup=tel_keyboard.rent_min_setting_replykeyboard())
        bot.register_next_step_handler(msg, rent_max_chat)

    def rent_max_chat(message):
        min_price = message.text
        users[f'{message.chat.id}']["min_price"] = min_price
        msg = bot.send_message(chat_id=message.chat.id,
                               text='*Ограничения цены* \nВыберите или напишите максимальную цену недвижимости?',
                               reply_markup=tel_keyboard.rent_max_setting_replykeyboard())
        bot.register_next_step_handler(msg, close_dialog)

    @bot.message_handler(content_types=["text"])
    def sell_min_chat(message):
        count_room = message.text
        users[f'{message.chat.id}']["count_room"] = count_room
        msg = bot.send_message(chat_id=message.chat.id,
                               text='*Ограничения цены* \nВыберите или напишите минимальную цену недвижимости?',
                               reply_markup=tel_keyboard.sell_min_setting_replykeyboard())
        bot.register_next_step_handler(msg, sell_max_chat)

    @bot.message_handler(content_types=["text"])
    def sell_max_chat(message):
        min_price = message.text
        users[f'{message.chat.id}']["min_price"] = min_price
        msg = bot.send_message(chat_id=message.chat.id,
                               text='*Ограничения цены* \nВыберите или напишите максимальную цену недвижимости?',
                               reply_markup=tel_keyboard.sell_max_setting_replykeyboard())
        bot.register_next_step_handler(msg, close_dialog)

    @bot.message_handler(content_types=["text"])
    def close_dialog(message):
        max_price = message.text
        users[f'{message.chat.id}']["max_price"] = max_price
        keyboard = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "Настройки сохранены.", reply_markup=keyboard)
        keyboard_btn = types.InlineKeyboardMarkup()
        okbtn = types.InlineKeyboardButton(text='OK', callback_data='okbtn')
        settings_btn = types.InlineKeyboardButton(text='Настроить', callback_data='filter_settings')
        keyboard_btn.add(okbtn, settings_btn)
        if users[f"{message.chat.id}"]["min_price"] == "Нет" and users[f"{message.chat.id}"]["max_price"] == "Нет":
            bot.send_message(chat_id=message.chat.id,
                             text=f'*Критерии поиска* \n\n*Типа дома*: {users[f"{message.chat.id}"]["house_type"]};\n*Тип объявления*: {users[f"{message.chat.id}"]["ad_type"]};\n*Количество комнат*: {users[f"{message.chat.id}"]["count_room"]}.',
                             reply_markup=keyboard_btn)
        elif users[f"{message.chat.id}"]["min_price"] == "Нет" and users[f"{message.chat.id}"]["max_price"] != "Нет":
            bot.send_message(chat_id=message.chat.id,
                             text=f'*Критерии поиска* \n\n*Типа дома*: {users[f"{message.chat.id}"]["house_type"]};\n*Тип объявления*: {users[f"{message.chat.id}"]["ad_type"]};\n*Количество комнат*: {users[f"{message.chat.id}"]["count_room"]};\n*Цена*: до {users[f"{message.chat.id}"]["max_price"]} руб.',
                             reply_markup=keyboard_btn)
        elif users[f"{message.chat.id}"]["min_price"] != "Нет" and users[f"{message.chat.id}"]["max_price"] == "Нет":
            bot.send_message(chat_id=message.chat.id,
                             text=f'*Критерии поиска* \n\n*Типа дома*: {users[f"{message.chat.id}"]["house_type"]};\n*Тип объявления*: {users[f"{message.chat.id}"]["ad_type"]};\n*Количество комнат*: {users[f"{message.chat.id}"]["count_room"]};\n*Цена*: от {users[f"{message.chat.id}"]["min_price"]} руб.',
                             reply_markup=keyboard_btn)
        else:
            bot.send_message(chat_id=message.chat.id,
                             text=f'*Критерии поиска* \n\n*Типа дома*: {users[f"{message.chat.id}"]["house_type"]};\n*Тип объявления*: {users[f"{message.chat.id}"]["ad_type"]};\n*Количество комнат*: {users[f"{message.chat.id}"]["count_room"]};\n*Цена*: от {users[f"{message.chat.id}"]["min_price"]} до {users[f"{message.chat.id}"]["max_price"]} руб.',
                             reply_markup=keyboard_btn)


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
        with open("users.json", encoding='utf-8') as file:
            users = json.load(file)
        telegram_keyboard(bot, users)

    bot.polling()


if __name__ == '__main__':
    main()
