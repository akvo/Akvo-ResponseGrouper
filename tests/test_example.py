import unittest

from AkvoResponseGrouper.example import Example


class TestExample(unittest.TestCase):
    def test_add(self):
        self.assertEqual((Example(5) + Example(6)).value, 11)


if __name__ == '__main__':
    unittest.main()
