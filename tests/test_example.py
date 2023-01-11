import unittest

from AkvoResponseGrouper import response_grouper
import AkvoResponseGrouper


class TestExample(unittest.TestCase):
    def test_show_all_classes(self):
        print(help(AkvoResponseGrouper))

    def test_add(self):
        self.assertEqual((response_grouper(5) + response_grouper(6)).value, 11)


if __name__ == '__main__':
    unittest.main()
