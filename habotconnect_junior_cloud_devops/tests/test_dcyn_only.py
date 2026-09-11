import unittest

from app.dcyn import DCYNValidationError, parse_dcyn


class DCYNOnlyTests(unittest.TestCase):
    def test_yes(self):
        self.assertIs(parse_dcyn("Yes"), True)

    def test_no(self):
        self.assertIs(parse_dcyn("No"), False)

    def test_invalid(self):
        with self.assertRaises(DCYNValidationError):
            parse_dcyn("Maybe")


if __name__ == "__main__":
    unittest.main()
