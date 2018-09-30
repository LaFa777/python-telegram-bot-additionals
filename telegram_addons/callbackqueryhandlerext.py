from telegram.ext import CallbackQueryHandler


class CallbackQueryHandlerExt:

    def __init__(self,
                 command=None,
                 *args,
                 **kwargs):
        self.command = command or ""
        self.handler = CallbackQueryHandler(*args, **kwargs)
