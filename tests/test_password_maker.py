import os
import string
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import password_maker as pm  # noqa: E402


class TestPassword(unittest.TestCase):
    def test_length(self):
        for n in (4, 8, 16, 64):
            self.assertEqual(len(pm.generate_password(n)), n)

    def test_contains_every_group(self):
        for _ in range(200):
            pw = pm.generate_password(8)
            self.assertTrue(any(c in string.ascii_lowercase for c in pw))
            self.assertTrue(any(c in string.ascii_uppercase for c in pw))
            self.assertTrue(any(c in string.digits for c in pw))
            self.assertTrue(any(c in pm.SYMBOLS for c in pw))

    def test_digits_only(self):
        pw = pm.generate_password(12, lower=False, upper=False, symbols=False)
        self.assertTrue(pw.isdigit())

    def test_no_ambiguous(self):
        for _ in range(100):
            pw = pm.generate_password(50, no_ambiguous=True)
            self.assertFalse(set(pw) & pm.AMBIGUOUS)

    def test_no_groups_raises(self):
        with self.assertRaises(ValueError):
            pm.generate_password(10, False, False, False, False)

    def test_too_short_raises(self):
        with self.assertRaises(ValueError):
            pm.generate_password(3)

    def test_randomness(self):
        self.assertEqual(len({pm.generate_password(16) for _ in range(100)}), 100)


class TestPassphrase(unittest.TestCase):
    def test_word_count(self):
        self.assertEqual(len(pm.generate_passphrase(5).split("-")), 5)

    def test_separator_and_number(self):
        parts = pm.generate_passphrase(3, separator=".", add_number=True).split(".")
        self.assertEqual(len(parts), 4)
        self.assertTrue(parts[-1].isdigit())

    def test_capitalize(self):
        for w in pm.generate_passphrase(4, capitalize=True).split("-"):
            self.assertTrue(w[0].isupper())


class TestStrength(unittest.TestCase):
    def test_labels(self):
        self.assertEqual(pm.strength_label(pm.entropy_bits("abc")), "Zayıf")
        self.assertEqual(pm.strength_label(pm.entropy_bits(pm.generate_password(20))),
                         "Çok güçlü")


class TestCLI(unittest.TestCase):
    def test_main_ok(self):
        self.assertEqual(pm.main(["-l", "10", "-n", "2"]), 0)

    def test_main_error(self):
        self.assertEqual(pm.main(["--no-lower", "--no-upper", "--no-digits",
                                  "--no-symbols"]), 2)


if __name__ == "__main__":
    unittest.main()
