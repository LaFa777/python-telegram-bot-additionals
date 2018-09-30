import hashlib


def hash64(s):
    """Вычисляет хеш - 8 символов (64 бита)
    """
    hex = hashlib.sha1(s.encode("utf-8")).hexdigest()
    return "{:x}".format(int(hex, 16) % (10 ** 8))


class CallbackDataSerializer:
    """Инкапслуриует алгоритм хеширования и пасринга параметра ``callback_data`` для объектов типа
    ``InlineKeyboardButtonExt``. Неявно используется в компонентах (сабклассах ``ComponentHandler``)
    для создания уникальной хеш-маски.
    """

    def __init__(self, name=""):
        """
        Attributes:
            salt (`str`): Любое строковое значение
        """
        self._name = name
        self.reset()

    def reset(self):
        """Сбрасывает все параметры
        """
        self._name = ""
        self._command = ""
        self._data = ""

    def set_name(self, name):
        """Устанавливает соль для последующего хеширования
        """
        self._name = name

        # fluent interface
        return self

    def set_command(self, command):
        """Устанавливает строковое значение, которое будет использоваться в формировании хеша.
        """
        self._command = command

        # fluent interface
        return self

    def set_data(self, data):
        """Устанавливает данные, которые не будут хешированы и будут переданы как есть.
        """
        if data is not None and len(data) >= 55:
            raise ValueError("callback_data too long ({} symbols). "
                             "Please reduce to 55 bytes(symbols)".format(len(data)))

        self._data = data

        # fluent interface
        return self

    def dumps(self, only_hash=False):
        """Создает строку формата "hash:data", где:
          hash - уникальный хеш (соль + команда) (8 символов)
          data - данные (0-55 символа)

        Attributes:
            only_hash (``bool``): выводить только "hash:" (нужно для ``CallbackQueryHandlerExt``)
        """
        # нет смысла хешировать если не задано ключевое значение для хеширования
        if not self._name:
            raise ValueError("Please setup \"name\" parametr using \".set_name(name)\".")

        hash_value = self._name
        if self._command:
            hash_value = hash_value + self._command
        hash_str = hash64(hash_value)

        if only_hash:
            return "{}:".format(hash_str)
        else:
            return "{}:{}".format(hash_str, self._data)

    def loads(self, callback_data):
        """Возвращает строку, из которой вырезан "hash:" и оставлены только "data".
        """
        return callback_data.split(":", 1)[1]
