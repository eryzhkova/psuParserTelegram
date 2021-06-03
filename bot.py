from auth_data import TOKEN
import telebot
from telebot import types
from keyboard import TelegramKeyboards

def telegram_keyboard(token):
    bot = telebot.TeleBot(token, parse_mode='Markdown')
    count_site = 0
    city = "Пермь"
    tel_keyboard = TelegramKeyboards(count_site, city)

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
        settings_btn = types.InlineKeyboardButton(text='Посмотреть настройки', callback_data='settings')
        keyboard.add(settings_btn)
        bot.send_message(message.chat.id,
                         '*Раздел настроек*',
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
    def callback_worker_promo(call):
        bot.send_message(call.message.chat.id,
                         '*Критерии поиска* \nЗдесь ты можешь посмотреть настройки своего запроса '
                         'или изменить их',
                         reply_markup=tel_keyboard.main_setting_keyboard())

    @bot.callback_query_handler(func=lambda call: call.data.startswith('sites'))
    def callback_worker_promo(call):
        bot.send_message(call.message.chat.id,
                         '*Сайты объявлений* \nЗдесь ты можешь посмотреть свои настройки, '
                         'связанные с сайтами, где искать объявления',
                         reply_markup=tel_keyboard.sites_setting_keyboard())

    bot.polling()

if __name__ == '__main__':
    telegram_keyboard(TOKEN)
