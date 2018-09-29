from telegram.ext import Updater
from inputage import InputAge
from inputnumber import InputNumber


# включаем логгирование
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    updater = Updater("TOKEN")

    dispatcher = updater.dispatcher

    InputAge(dispatcher)
    InputNumber(dispatcher)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
