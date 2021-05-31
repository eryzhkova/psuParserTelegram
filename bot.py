import requests
import telebot

from auth_data import TOKEN

# requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage', params={'chat_id': id, 'text': 'text!'})

def telegrambot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(content_types=['text'])
    def check_id_name(message):
        print(message.from_user.id)
        print(message.chat.id)
        print(message.from_user.first_name)
        print(message.text)

    bot.polling()


if __name__ == '__main__':
    telegrambot(TOKEN)
