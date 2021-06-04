from auth_data import TOKEN
import telebot


class UserChat:
    bot = telebot.TeleBot(TOKEN, parse_mode='Markdown')

    def __init__(self, call, keyboard):
        self.call = call
        self.keyboard = keyboard

    def house_chat(self):
        self.bot.send_message(chat_id=self.call.message.chat.id,
                              text='*Тип дома* \nКакой тип недвижимости Вас интересует?',
                              reply_markup=self.keyboard.house_setting_replykeyboard())
        return self.call.message.text

    # def ad_chat(self):
    #     self.bot.send_message(chat_id=self.call.message.chat.id,
    #                           text='*Тип объявления* \nХотите купить или снимать?',
    #                           reply_markup=self.keyboard.ad_setting_replykeyboard())
    #     return self.call.message.text
    #
    # def room_chat(self):
    #     self.bot.send_message(chat_id=self.call.message.chat.id,
    #                           text='*Количество комнат* \nКакое количество комнат? \nМожете выбрать из предложанных '
    #                                'или ввести одну цифру, либо несколько через запятую (",") или дефис ("-").',
    #                           reply_markup=self.keyboard.room_setting_replykeyboard())
    #     return self.call.message.text
    #
    # def rent_min_chat(self):
    #     self.bot.send_message(chat_id=self.call.message.chat.id,
    #                           text='*Ограничения цены* \nВыберите или напишите минимальную цену недвижимости?',
    #                           reply_markup=self.keyboard.rent_min_setting_replykeyboard())
    #     return self.call.message.text
    #
    # def rent_max_chat(self):
    #     self.bot.send_message(chat_id=self.call.message.chat.id,
    #                           text='*Ограничения цены* \nВыберите или напишите максимальную цену недвижимости?',
    #                           reply_markup=self.keyboard.rent_max_setting_replykeyboard())
    #     return self.call.message.text
    #
    # def sell_min_chat(self):
    #     self.bot.send_message(chat_id=self.call.message.chat.id,
    #                           text='*Ограничения цены* \nВыберите или напишите минимальную цену недвижимости?',
    #                           reply_markup=self.keyboard.sell_min_setting_replykeyboard())
    #     return self.call.message.text
    #
    # def sell_max_chat(self):
    #     self.bot.send_message(chat_id=self.call.message.chat.id,
    #                           text='*Ограничения цены* \nВыберите или напишите максимальную цену недвижимости?',
    #                           reply_markup=self.keyboard.sell_max_setting_replykeyboard())
    #     return self.call.message.text
