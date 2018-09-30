from telegram import InlineKeyboardButton


class InlineKeyboardButtonExt(InlineKeyboardButton):
    """Добавляет возможность более точно указать обработчика используя
    `telegram.CallbackQueryHandlerExt` путем указания параметра command.
    Параметр command используется для последующего преобразования ``callback_data`` в ``BotProxy``.
    """

    def __init__(self, text, command=None, *args, **kwargs):
        self.command = command
        super().__init__(text, *args, **kwargs)

    def to_dict(self):
        # command не является параметром для api телеграма
        if "command" in self.__dict__:
            del self.command
        return super().to_dict()
