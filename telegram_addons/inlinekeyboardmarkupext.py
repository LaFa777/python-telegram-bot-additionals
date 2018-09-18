from telegram import InlineKeyboardMarkup


class InlineKeyboardMarkupExt(InlineKeyboardMarkup):
    """Переопределяет инициализатор :class:`telegram.InlineKeyboardMarkup`, добавляя возможность
    отложенного добавления разметки.
    """

    def __init__(self, inline_keyboard=None, **kwargs):
        inline_keyboard = inline_keyboard or []
        super().__init__(inline_keyboard, **kwargs)

    def add_line(self, *buttons):
        """Добавляет строку меню с указанными `buttons` (объектами типа
        :class:`telegram.InlineKeyboardButton`)
        """
        self.inline_keyboard.append(buttons)
