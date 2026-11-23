
import sys
import unittest

from pathlib import Path
import string

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1]),
)

from password_generator import generate_password


class TestPasswordGenerator(unittest.TestCase):

    def test_generated_password_has_requested_length(self):
        password = generate_password(24)

        self.assertEqual(len(password), 24)

    def test_generated_password_contains_character_types(self):
        password = generate_password(20)

        self.assertTrue(
            any(char in string.ascii_lowercase for char in password)
        )

        self.assertTrue(
            any(char in string.ascii_uppercase for char in password)
        )

        self.assertTrue(
            any(char in string.digits for char in password)
        )

    def test_password_length_must_be_at_least_four(self):
        with self.assertRaises(ValueError):
            generate_password(3)


if __name__ == "__main__":
    unittest.main()
