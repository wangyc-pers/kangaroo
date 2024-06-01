import unittest
from app.utils.base58_utils import int_to_str, str_to_int


class Base58UtilsTestCase(unittest.TestCase):
    def test_int_to_str_positive(self):
        self.assertEqual(int_to_str(1725862), "9r3F")
        self.assertEqual(int_to_str(500817, prefix="ID"), "ID_3Zsn")
        self.assertEqual(int_to_str(357263, prefix="ID", sep="-"), "ID-2qCi")

    def test_int_to_str_zero(self):
        self.assertEqual(int_to_str(0), "1")

    def test_int_to_str_negative(self):
        self.assertEqual(int_to_str(-123), "")

    def test_str_to_int_positive(self):
        self.assertEqual(str_to_int("_2V"), 86)
        self.assertEqual(str_to_int("ID_3u", sep="_"), 168)
        self.assertEqual(str_to_int("-4r", sep="-"), 223)

    def test_str_to_int_empty(self):
        self.assertEqual(str_to_int(""), -1)

    def test_str_to_int_invalid(self):
        self.assertEqual(str_to_int("invalid"), -1)