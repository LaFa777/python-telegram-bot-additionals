import copy

from telegram.ext import Handler

from .callbackdataserializer import CallbackDataSerializer
from .simplehandler import SimpleHandler
from .dispatcherproxy import DispatcherProxy, wrapped_bot_and_update_proxy
from .botproxy import BotProxy


class ComponentHandler(SimpleHandler):
    """Модуль для обработки сложных действий и возврате данных по окончанию.

    Всегда имеет точку входа `.start()` - будьте готовы, что модуль имеет полное
    право затенить существующе обработчики или немного изменить работу бота.
    (например при активации модуля получения ввода модуль начинает обрабатывать
    любой текстовый ввод от пользователя)

    По окончанию работы модуль в своей завершающей функции вызывает `notify`,
    которая в свою очередь передает всем коллбекам переданным ранее в
    `add_done_callback()` данные о результате работы. Формат даннных не
    унифицирован и индивидуален у каждого модуля (читайте в описании к модулю).
    """

    def __init__(self,
                 component_name,
                 dispatcher,
                 bind_handlers=True,
                 callback_data_serializer=None):

        if callback_data_serializer:
            self._callback_data_serializer = copy.copy(callback_data_serializer)
        else:
            self._callback_data_serializer = CallbackDataSerializer()

        self._callback_data_serializer.set_name(component_name)

        self._component_name = component_name

        # если dispatcher is DispatcherProxy, то скопируем, а не наследуем, дабы избежать
        # многократного выполнения DispatcherProxy.add_handler
        if isinstance(dispatcher, DispatcherProxy):
            dispatcher = copy.copy(dispatcher)
            dispatcher._callback_data_serializer = self._callback_data_serializer
        else:
            dispatcher = DispatcherProxy(dispatcher, self._callback_data_serializer)

        self._done_callbacks = []

        super().__init__(dispatcher, bind_handlers)

    def start(self, bot, update):
        start_func = wrapped_bot_and_update_proxy(self._callback_data_serializer, self._start)
        start_func(bot, update)

    def _start(self, bot, update):
        """Каждый компонент обязан иметь данную точку входа.
        """
        raise NotImplementedError

    def add_done_callback(self,
                          callback,
                          pass_update_queue=False,
                          pass_job_queue=False,
                          pass_user_data=False,
                          pass_chat_data=False):
        """Добавляет функцию обработчик, в которую по окончанию передаются данные
        работы компонента.
        """
        handler = Handler(callback, pass_update_queue, pass_job_queue,
                          pass_user_data, pass_chat_data)
        self._done_callbacks.append(handler)

    def notify(self, bot, update, data):
        """Оповещает функцию обратного вызова о завершении работы компонента и передает в нее данные

        Если переданный метод является членом экземпляра ``ComponentHandler``, то ему сразу
        проставляем ему корректный экземпляр BotProxy.
        """
        # достаем оригинальный ``telegram.Bot``
        if isinstance(bot, BotProxy):
            bot = bot._bot

        for handler in self._done_callbacks:
            # для инстансов ComponentHandler необходимо обеспечить
            # корректное прозрачное проксирование BotProxy
            callback = handler.callback
            if isinstance(callback.__self__, ComponentHandler):
                serializer = callback.__self__._callback_data_serializer
                callback = wrapped_bot_and_update_proxy(serializer, callback)

            # формируем опциональные аргументы (например: pass_user_data)
            optional_args = handler.collect_optional_args(self._dispatcher, update)

            callback(bot, update, data, **optional_args)
