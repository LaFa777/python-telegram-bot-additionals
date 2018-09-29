from telegram_addons import (
    ComponentHandler,
    InlineKeyboardButtonExt,
    InlineKeyboardMarkupExt,
    TextMessage,
    CallbackQueryHandlerExt,
)


class CounterCommands:
    SHOW = "SHOW"
    DONE = "DONE"


class CounterComponent(ComponentHandler):
    """Пример реализации компонента, для ввода числа, используя кнопки.
    """

    def __init__(self, dispatcher, namespace, message_text):
        self.message_text = message_text
        component_name = namespace + "_counter"
        super().__init__(component_name, dispatcher)

    def bind_handlers(self, dispatcher):
        handler = CallbackQueryHandlerExt(CounterCommands.SHOW, self.counter_show)
        dispatcher.add_handler(handler)

        handler = CallbackQueryHandlerExt(CounterCommands.DONE, self.counter_done)
        dispatcher.add_handler(handler)

    def _start(self, bot, update):
        self.counter_show(bot, update)

    def counter_show(self, bot, update, number=0):
        if update.callback_query:
            number = update.callback_query.data

        tg_message = self.message(number)

        message = update.effective_message
        if update.callback_query:
            bot.edit_message_text(chat_id=message.chat_id,
                                  message_id=message.message_id,
                                  **tg_message)
        else:
            bot.send_message(chat_id=message.chat_id,
                             **tg_message)

    def counter_done(self, bot, update):
        number = update.callback_query.data

        # Работа закончена. Оповещаем родительский модуль об окончании работы
        self.notify(bot, update, number)

    def message(self, number):
        number = int(number)

        keyboard = InlineKeyboardMarkupExt()

        button_reduce = InlineKeyboardButtonExt(text="<",
                                                command=CounterCommands.SHOW,
                                                callback_data=str(number-1))
        button_add = InlineKeyboardButtonExt(text=">",
                                             command=CounterCommands.SHOW,
                                             callback_data=str(number+1))
        keyboard.add_line(button_reduce, button_add)

        button_reset = InlineKeyboardButtonExt(text="reset",
                                               command=CounterCommands.SHOW,
                                               callback_data="0")
        keyboard.add_line(button_reset)

        button_done = InlineKeyboardButtonExt(text="done",
                                              command=CounterCommands.DONE,
                                              callback_data=str(number))
        keyboard.add_line(button_done)

        text = "{}\n{}".format(self.message_text, number)

        return TextMessage(text, reply_markup=keyboard)
