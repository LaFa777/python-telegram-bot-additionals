import random

from telegram.ext import CommandHandler
from telegram_addons import SimpleHandler
from countercomponent import CounterComponent


class InputNumber(SimpleHandler):

    def __init__(self, dispatcher):
        self._counter = CounterComponent(dispatcher, "number", "Введи любое число:")
        super().__init__(dispatcher)

    def bind_handlers(self, dispatcher):
        dispatcher.add_handler(CommandHandler("number", self.number_start, pass_user_data=True))
        self._counter.add_done_callback(self.number_done, pass_user_data=True)

    def number_start(self, bot, update, user_data):
        user_data["number"] = random.randint(0, 3)
        update.message.reply_text("Введи любое число и я скажу угадал ты или нет")
        self._counter.start(bot, update)

    def number_done(self, bot, update, number, user_data):
        if int(number) == int(user_data["number"]):
            text = "Ты отгадал!\nЗагаданное число - {}".format(number)
        else:
            text = "Неправильно.\nЯ загадал число - {}\nВаш ответ - {}".format(
                user_data["number"], number)

        update.effective_message.reply_text(text)
