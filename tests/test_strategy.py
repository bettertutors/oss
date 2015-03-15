from unittest import TestCase, main as unittest_main

from oss.parse_strategy import parse_strategy


class TestParseStrategy(TestCase):
    strategy = parse_strategy()

    def test_env(self):
        # Just tests if it has been substituted, doesn't check correctness of substitution
        map(lambda item: self.assertNotIn('env', item[1]), self.strategy['provider']['primary']['auth'].iteritems())

    def test_caps(self):
        self.assertEqual(*(lambda val: (val, val.upper()))(self.strategy['provider']['primary']['name']))


if __name__ == '__main__':
    unittest_main()
