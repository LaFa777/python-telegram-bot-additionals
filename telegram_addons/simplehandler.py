class SimpleHandler:
    """Предназначен для обработки простейших событий.

    При субклассировании должны быть реализованы:
    1. Функция bind_handlers, цепляющая обработчики к dispatcher.
    2. Коолбеки, к которым происходит биндинг в bind_handlers

    Пример:
        >>> class HelpHandler(SimpleHandler):
        ...
        ...   def bind_handlers(self, dispatcher):
        ...     dispatcher.add_handler(CommandHandler("help", help))
        ...
        ...   def help(self, bot, update):
        ...     update.message.reply_text("Type /start for start")
        ...
        >>> HelpHandler(dispatcher)
        >>> dispatcher.start_polling()
    """

    def __init__(self, dispatcher, bind_handlers=True):
            """
            Attributes:
                dispatcher (:class:`telegram.ext.Dispatcher`)
                bind_handlers (`bool`): вызывать ли функцию `bind_handlers` при инициализации класса.
            """
            self._dispatcher = dispatcher
            if bind_handlers:
                self.bind_handlers(self._dispatcher)

    def bind_handlers(self, dispatcher):
        """В эту функцию помещается код для связывания обработчиков.
        """
        raise NotImplementedError
