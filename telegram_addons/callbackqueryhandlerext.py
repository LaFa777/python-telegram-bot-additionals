from telegram.ext import CallbackQueryHandler


class CallbackQueryHandlerExt:

    def __init__(self,
                 command,
                 *args,
                 **kwargs):
        self.command = command
        self.handler = CallbackQueryHandler(*args, **kwargs)
