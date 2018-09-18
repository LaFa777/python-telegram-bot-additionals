# python-telegram-bot-addons
Небор расширений для библиотеки [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

#### TextMessage

Просто удобная обертка для передачи параметров методам `telegram.bot.send_*`, `telegram.bot.edit_*`
 и `telegram.Message.reply_text()`

Пример:
```
message = TextMessage("Hello world!", reply_markup=generate_markup)
update.message.reply_text(**message)
```

## Компоненты

#### SimpleHandler

Удобный способ структурирования кода. Все связанные по смыслу обработчики помещаются в наследника
 данного класса.

```
class HelpHandler(SimpleHandler):

  def bind_handlers(self, dispatcher):
    dispatcher.add_handler(CommandHandler("help", help))

  def help(self, bot, update):
    update.message.reply_text("Type /start for start")
```
