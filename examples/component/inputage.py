from telegram.ext import CommandHandler
from telegram_addons import SimpleHandler
from countercomponent import CounterComponent


class InputAge(SimpleHandler):

    def __init__(self, dispatcher):
        self._counter = CounterComponent(dispatcher, "age", "Введи свой возраст:")
        super().__init__(dispatcher)

    def bind_handlers(self, dispatcher):
        dispatcher.add_handler(CommandHandler("age", self.age_start))
        self._counter.add_done_callback(self.age_done)

    def age_start(self, bot, update):
        self._counter.start(bot, update)

    def age_done(self, bot, update, age):
        update.effective_message.reply_text("Тебе {} лет".format(age))
