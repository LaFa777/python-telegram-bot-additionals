# python-telegram-bot-addons
Небор расширений для библиотеки [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

#### TextMessage

Просто удобная обертка для передачи параметров методам `telegram.bot.send_*`, `telegram.bot.edit_*`
 и `telegram.Message.reply_text()`

```Python
message = TextMessage("Hello world!", reply_markup=generate_markup)
update.message.reply_text(**message)
```

## Компоненты

#### SimpleHandler

Удобный способ структурирования кода. Все связанные по смыслу обработчики помещаются в наследника
 данного класса.

```Python
class HelpHandler(SimpleHandler):

  def bind_handlers(self, dispatcher):
    dispatcher.add_handler(CommandHandler("help", help))

  def help(self, bot, update):
    update.message.reply_text("Type /start for start")

HelpHandler(dispatcher)
dispatcher.start_polling()
```

#### InlineKeyboardMarkupExt

Переопределяет `InlineKeyboardMarkup`, добавляя возможность
отложенного добавления разметки.

```Python
keyboard = InlineKeyboardMarkupExt()

button1 = InlineKeyboardButton("1", callback_data='1')
button2 = InlineKeyboardButton("2", callback_data='2')
keyboard.add_line(button1, button2)

button_ok = InlineKeyboardButton("save", callback_data='save')
keyboard.add_line(button_ok)

message = TextMessage("Example `InlineKeyboardMarkupExt`",
                      parse_mode="Markdown",
                      reply_markup=keyboard)
```

![pic](./assets/inlinekeyboardmarkupext.png)
