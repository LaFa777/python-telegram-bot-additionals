import functools

from telegram import InlineKeyboardMarkup

from .inlinekeyboardbuttonext import InlineKeyboardButtonExt


def message_callback_data_serializer(serializer, func):
    """Модифицированная версия декоратора `telegram.bot.message` для работы с
    ``InlineKeyboardButtonExt``
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        # преобразуем callback_data для всех InlineKeyboardButtonExt
        if kwargs.get('reply_markup'):
            reply_markup = kwargs['reply_markup']
            if isinstance(reply_markup, InlineKeyboardMarkup):
                for buttons in reply_markup.inline_keyboard:
                    for button in buttons:
                        if isinstance(button, InlineKeyboardButtonExt):
                            button.callback_data = serializer\
                                .set_command(button.command)\
                                .set_data(button.callback_data)\
                                .dumps()
        return func(*args, **kwargs)
    return decorator


class BotProxy:
    """Attribute proxy для `telegram.Bot`
    """

    wrapped_methods = [
        "send_message",
        "edit_message_text",
        "forward_message",
        "send_photo",
        "send_audio",
        "send_document",
        "send_sticker",
        "send_video",
        "send_video_note",
        "send_animation",
        "send_voice",
        "send_location",
        "edit_message_live_location",
        "stop_message_live_location",
        "send_venue",
        "send_contact",
        "send_game",
        "edit_message_caption",
        "edit_message_media",
        "edit_message_reply_markup",
        "set_game_score",
        "send_invoice",
    ]

    def __init__(self, bot, callback_data_serializer):
        self._bot = bot
        self._callback_data_serializer = callback_data_serializer

    def __getattr__(self, name):
        if name in self.wrapped_methods:
            wrap_func = message_callback_data_serializer(
                    self._callback_data_serializer,
                    getattr(self._bot, name))
            return wrap_func
        else:
            return getattr(self._bot, name)
