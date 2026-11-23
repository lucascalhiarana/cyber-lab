import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest

from cryptography.exceptions import InvalidTag

from crypto import generate_salt, derive_key, encrypt_data, decrypt_data


class TestCrypto(unittest.TestCase):

    def test_encryption_and_decryption(self):
        password = "MasterPassword123!"
        original_data = b"My secret password"

        salt = generate_salt()
        key = derive_key(password, salt)

        nonce, ciphertext = encrypt_data(original_data, key)

        decrypted_data = decrypt_data(nonce, ciphertext, key)

        self.assertEqual(decrypted_data, original_data)

    def test_wrong_key_fails(self):
        original_data = b"My secret password"

        salt = generate_salt()
        key = derive_key("CorrectPassword", salt)
        wrong_key = derive_key("WrongPassword", salt)

        nonce, ciphertext = encrypt_data(original_data, key)

        with self.assertRaises(InvalidTag):
            decrypt_data(nonce, ciphertext, wrong_key)

if __name__ == "__main__":
    unittest.main()
    