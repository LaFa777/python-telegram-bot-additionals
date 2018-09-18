import unittest

from telegram_addons import CallbackDataSerializer


class TestCallbackDataSerializer(unittest.TestCase):

    def test_dumps(self):
        hash_str = "26f0e66:"

        ds = CallbackDataSerializer()
        ds.set_salt("some_component")
        ds.set_command("add")
        self.assertEqual(ds.dumps(), hash_str)

        ds.set_command("del")
        self.assertNotEqual(ds.dumps(), hash_str)

        ds.set_command("add")
        self.assertEqual(ds.dumps(), hash_str)

    def test_loads(self):
        data = "12345"

        ds = CallbackDataSerializer()
        ds.set_salt("some_component")
        ds.set_command("add")
        ds.set_data(data)

        hash_callback_data = ds.dumps()

        load_data = ds.loads(hash_callback_data)

        self.assertEqual(load_data, data)

    def test_dumps_raise(self):
        with self.assertRaises(ValueError):
            CallbackDataSerializer().dumps()


if __name__ == '__main__':
    unittest.main()
