from telegram.ext import ConversationHandler


class ConversationHandlerExt(ConversationHandler):
    """Расширяет оригинальный :class:`telegram.ext.ConversationHandler` возможностью вручную
    установить `state`. Переопределяет конструктор, теперь обязателен только 1 параметр (states).
    """

    def __init__(self,
                 states,
                 **kwargs):
        if 'entry_points' not in kwargs:
            kwargs["entry_points"] = []
        if 'fallbacks' not in kwargs:
            kwargs["fallbacks"] = []

        kwargs["states"] = states

        super().__init__(**kwargs)

    def set_state(self, update, state):
        """Устанавливает переданный state.
        """
        # проверяем, что переданный state возможен
        if state not in self.states.keys() and state != self.END:
            raise ValueError(
                "state=\"{}\" not exist in current ConversationHandlerExt".format(state))

        key = self._get_key(update)
        self.update_state(state, key)
