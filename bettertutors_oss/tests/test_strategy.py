from unittest import TestCase, main as unittest_main
from json import dumps

from bettertutors_oss.parse_strategy import parse_strategy


class TestParseStrategy(TestCase):
    strategy = parse_strategy()

    def test_env(self):
        # Just tests if it has been substituted, doesn't check correctness of substitution
        self.assertNotIn('env', dumps(self.strategy))

    def test_caps(self):
        """ Test if provider name is correctly capitalised """
        self.assertEqual(
            filter(None, map(lambda provider: (lambda key: self.assertEqual(key.upper(), key))(provider.keys()[0]),
                             self.strategy['provider']['options'])),
            []
        )


if __name__ == '__main__':
    unittest_main()
