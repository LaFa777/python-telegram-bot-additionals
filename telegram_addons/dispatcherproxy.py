import functools

from telegram.ext import (
    Dispatcher,
    ConversationHandler,
)

from .botproxy import BotProxy
from .callbackqueryhandlerext import CallbackQueryHandlerExt


def callback_data_unserialized(serializer, func):
    """Убирает из callback_query.data конструкцию "hash:"
    """
    @functools.wraps(func)
    def decorator(bot, update, *args, **kwargs):
        update.callback_query.data = serializer.loads(update.callback_query.data)
        return func(bot, update, *args, **kwargs)
    return decorator


def wrapped_bot_and_update_proxy(serializer, func):
    """Для ``ComponentHandler`` производит оборачивание аргументов ``bot`` и ``update`` в
    ``BotProxy``
    """
    @functools.wraps(func)
    def decorator(bot, update, *args, **kwargs):
        # если это прокси, то достаем оригинальый Bot обьект
        if isinstance(bot, BotProxy):
            bot = bot._bot
        bot = BotProxy(bot, serializer)

        if update.message:
            update.message.bot = bot

        update.effective_message.bot = bot

        return func(bot, update, *args, **kwargs)
    return decorator


DEFAULT_GROUP = 0


class DispatcherProxy(Dispatcher):
    """Добавляет к диспатчеру функционал по замене объектов-контейнеров, для замены их на
    аналоги с возможностью запоминания состояния между перезапусками скрипта.
    Поддержку расширенных обработчиков (имеющих постфикс `Ext`)
    """

    def __init__(self,
                 dispatcher,
                 callback_data_serializer=None,
                 update_queue=None,
                 job_queue=None,
                 user_data=None,
                 chat_data=None,
                 conversations_data=None,
                 conversations_timeout_jobs=None):
        self._dispatcher = dispatcher
        self._callback_data_serializer = callback_data_serializer

        # для обеспечения сохранения данных между перезапусками скрипта будем использовать
        # контейнеры-прокси, с возможностью записи на диск и загрузки с диска.
        if update_queue:
            self._dispatcher.update_queue = update_queue.update(**dispatcher.update_queue)
        if job_queue:
            self._dispatcher.job_queue = job_queue.update(**dispatcher.job_queue)
        if user_data:
            self._dispatcher.user_data = user_data.update(**dispatcher.user_data)
        if chat_data:
            self._dispatcher.chat_data = chat_data.update(**dispatcher.chat_data)

        self._conversations_data = conversations_data
        self._conversations_timeout_jobs = conversations_timeout_jobs

    def add_handler(self, handler, group=DEFAULT_GROUP):
        serializer = self._callback_data_serializer

        # формируем корректный pattern в случае, если это `CallbackQueryHandlerExt`
        if isinstance(handler, CallbackQueryHandlerExt) and serializer:
            hash_str = serializer\
                .set_command(handler.command)\
                .dumps()
            handler.handler.pattern = hash_str
            handler = handler.handler

            # оборачиваем callback хандлера, чтобы он автоматически зачищал маску при обработке
            handler.callback = callback_data_unserialized(serializer, handler.callback)

        # в случае, если биндим `ConversationHandler`, то попытаем восстановить состояние до
        # перезапуска скрипта (загрузим переменные хранения)
        if isinstance(handler, ConversationHandler):
            if self._conversations_data:
                handler.conversations = self._conversations_data
            if self._conversations_timeout_jobs:
                handler.timeout_jobs = self._conversations_timeout_jobs

        # проксируем аргумент `telegram.Bot` для всех обработчиков
        # как правило serializer определен только для компонентов
        if serializer:
            handler.callback = wrapped_bot_and_update_proxy(serializer, handler.callback)

        self._dispatcher.add_handler(handler, group)

    def __getattr__(self, name):
        return getattr(self._dispatcher, name)
