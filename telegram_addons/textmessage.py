from collections import UserDict


class TextMessage(UserDict):
    """Просто удобная обертка над аргументами для функций типа :meth:`telegram.Bot.send_message`,
    :meth:`telegram.Bot.edit_message_text` или :meth:`telegram.Message.reply_text`.
    При передаче объект необходимо распаковать.
    """

    def __init__(self,
                 text,
                 chat_id=None,
                 message_id=None,
                 parse_mode=None,
                 disable_web_page_preview=None,
                 disable_notification=False,
                 reply_to_message_id=None,
                 reply_markup=None,
                 timeout=None,
                 **kwargs):
        data = dict()
        data["text"] = text
        if chat_id:
            data["chat_id"] = chat_id
        if message_id:
            data["message_id"] = message_id
        data["parse_mode"] = parse_mode
        data["disable_web_page_preview"] = disable_web_page_preview
        data["disable_notification"] = disable_notification
        data["reply_to_message_id"] = reply_to_message_id
        data["reply_markup"] = reply_markup
        data["timeout"] = timeout
        data.update(kwargs)
        self.data = data
