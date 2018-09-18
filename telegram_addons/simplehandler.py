class SimpleHandler:
    """Предназначен для обработки простейших событий.

    При субклассировании должны быть реализованы:
    1. Функция bind_handlers, цепляющая обработчики к dispatcher.
    2. Коолбеки, к которым происходит биндинг в bind_handlers
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
