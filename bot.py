from auth_data import TOKEN
import telebot
from telebot import types
from keyboard import TelegramKeyboards
from chat import UserChat


def telegram_keyboard(token):
    bot = telebot.TeleBot(token, parse_mode='Markdown')
    # TODO: Сделать словари для критериев
    # TODO: Собрать ошибки для исключений

    sites = ['Авито', 'Циан', 'Домофонд']

    count_sites = len(sites)
    city = "Пермь"
    house_type = "Новостройка"
    ad_type = "Продажа"
    count_room = "1"
    min_price = "0"
    max_price = "2000000"

    settings_text = f'\n\n*Сайты*: {count_sites};\n*Типа дома*: {house_type};\n*Тип объявления*: {ad_type};\n*Количество комнат*: {count_room};\n*Цена*: от {min_price} до {max_price} руб.;\n*Местоположение*: {city}.'

    tel_keyboard = TelegramKeyboards(count_sites, city)

    # Обработка команд
    @bot.message_handler(commands=["start"])
    def start_message(message):
        keyboard = types.InlineKeyboardMarkup()
        settings_btn = types.InlineKeyboardButton(text='Настроить нужный поиск', callback_data='settings')
        keyboard.add(settings_btn)
        bot.send_message(message.chat.id,
                         f'*Привет, {message.from_user.first_name}!* \nНастрой бота с помощью кнопки и получай '
                         f'обновления! \nЕсли кнопка не отображается '
                         'напиши боту команду */settings*',
                         reply_markup=keyboard)

    @bot.message_handler(commands=["settings"])
    def start_message(message):
        keyboard = types.InlineKeyboardMarkup()
        settings_btn = types.InlineKeyboardButton(text='Настроить', callback_data='settings')
        keyboard.add(settings_btn)
        bot.send_message(message.chat.id,
                         text='*Раздел настроек*' + settings_text,
                         reply_markup=keyboard)

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

    @bot.callback_query_handler(func=lambda call: call.data.startswith('confirmation'))
    def callback_confirmation(call):
        keyboard = types.InlineKeyboardMarkup()
        confirmation = types.InlineKeyboardButton(text='Подтвердить', callback_data='close_dialog')
        settings_btn = types.InlineKeyboardButton(text='Настроить', callback_data='settings')
        keyboard.add(confirmation, settings_btn)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='*Настройки* \nВаши настройки сохранены.' + settings_text,
                              reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('close_dialog'))
    def callback_close(call):
        bot.send_message(chat_id=call.message.chat.id,
                         text='*Все сохранено* \nИдет обработка запроса....')

    @bot.callback_query_handler(func=lambda call: call.data.startswith('filters'))
    def callback_filters(call):
        keyboard = types.InlineKeyboardMarkup()
        confirmation = types.InlineKeyboardButton(text='Подтвердить', callback_data='confirmation')
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
        user_chat = UserChat(call, tel_keyboard)
        house_type = user_chat.house_chat()
        if house_type == "Новостройка" or house_type == "Вторичка" or house_type == "Не важно":
            ad_type = user_chat.ad_chat()
            count_room = user_chat.room_chat()
            if ad_type == "Снимать":
                min_price = user_chat.rent_min_chat()
                max_price = user_chat.rent_max_chat()
            else:
                min_price = user_chat.sell_min_chat()
                max_price = user_chat.sell_max_chat()

        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(call.message.chat.id, "Все сохранено.", reply_markup=markup)

    bot.polling()


if __name__ == '__main__':
    telegram_keyboard(TOKEN)
