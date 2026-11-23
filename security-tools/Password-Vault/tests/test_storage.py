
import sys
import tempfile
import unittest

from pathlib import Path
from cryptography.exceptions import InvalidTag

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1]),
)

import storage
import main


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.temp_dir.name) / "vault.json"

        self.original_path = storage.VAULT_PATH
        storage.VAULT_PATH = self.test_path

    def tearDown(self):
        storage.VAULT_PATH = self.original_path
        self.temp_dir.cleanup()

    def test_encode_and_decode_bytes(self):
        original_data = b"Password Vault Test"

        encoded_data = storage.encode_bytes(original_data)
        decoded_data = storage.decode_bytes(encoded_data)

        self.assertEqual(decoded_data, original_data)

    def test_save_and_load_vault(self):
        vault_data = {
            "version": 1,
            "algorithm": "AES-256-GCM",
            "kdf": "Argon2id",
        }

        storage.save_vault(vault_data)
        loaded_data = storage.load_vault()

        self.assertEqual(loaded_data, vault_data)

    def test_build_vault_data(self):
        salt = b"test_salt"
        nonce = b"test_nonce"
        ciphertext = b"test_ciphertext"

        vault_data = storage.build_vault_data(
            salt,
            nonce,
            ciphertext,
        )

        self.assertEqual(vault_data["version"], 1)
        self.assertEqual(
            storage.decode_bytes(vault_data["salt"]),
            salt,
        )
        self.assertEqual(
            storage.decode_bytes(vault_data["nonce"]),
            nonce,
        )
        self.assertEqual(
            storage.decode_bytes(vault_data["ciphertext"]),
            ciphertext,
        )

    def test_create_and_open_vault(self):
        master_password = "TestMasterPassword123!"

        main.create_vault(master_password)

        vault_content = main.open_vault(master_password)

        self.assertEqual(vault_content, {})

    def test_wrong_master_password(self):
        main.create_vault("CorrectPassword123!")

        with self.assertRaises(InvalidTag):
            main.open_vault("WrongPassword123!")

    def test_cannot_create_existing_vault(self):
        main.create_vault("TestMasterPassword123!")

        with self.assertRaises(
            main.VaultAlreadyExistsError
        ):
            main.create_vault("AnotherPassword123!")

    def test_add_credential(self):
        vault_content = {}

        main.add_credential(
            vault_content,
            "GitHub",
            "my_user",
            "secret123",
        )

        self.assertEqual(
            vault_content["GitHub"]["username"],
            "my_user",
        )

        self.assertEqual(
            vault_content["GitHub"]["password"],
            "secret123",
        )

    def test_list_credentials(self):
        vault_content = {
            "GitHub": {},
            "Gmail": {},
        }

        result = main.list_credentials(vault_content)

        self.assertEqual(result, ["GitHub", "Gmail"])

    def test_get_credential(self):
        vault_content = {
            "GitHub": {
                "username": "my_user",
                "password": "secret123",
            },
        }

        result = main.get_credential(
            vault_content,
            "GitHub",
        )

        self.assertEqual(
            result["username"],
            "my_user",
        )

    def test_delete_credential(self):
        vault_content = {
            "GitHub": {
                "username": "my_user",
                "password": "secret123",
            },
        }

        main.delete_credential(
            vault_content,
            "GitHub",
        )

        self.assertNotIn("GitHub", vault_content)

    def test_save_and_open_credential(self):
        master_password = "TestMasterPassword123!"

        vault_content = {}

        main.add_credential(
            vault_content,
            "GitHub",
            "my_user",
            "secret123",
        )

        main.save_vault_content(
            vault_content,
            master_password,
        )

        recovered_content = main.open_vault(
            master_password,
        )

        self.assertEqual(
            recovered_content,
            vault_content,
        )

    def test_add_credential_to_vault(self):
        master_password = "TestMasterPassword123!"

        main.create_vault(master_password)

        main.add_credential_to_vault(
            master_password,
            "GitHub",
            "my_user",
            "secret123",
        )

        recovered_content = main.open_vault(
            master_password,
        )

        self.assertEqual(
            recovered_content["GitHub"]["username"],
            "my_user",
        )

        self.assertEqual(
            recovered_content["GitHub"]["password"],
            "secret123",
        )

    def test_delete_credential_from_vault(self):
        master_password = "TestMasterPassword123!"

        main.create_vault(master_password)

        main.add_credential_to_vault(
            master_password,
            "GitHub",
            "my_user",
            "secret123",
        )

        main.delete_credential_from_vault(
            master_password,
            "GitHub",
        )

        recovered_content = main.open_vault(
            master_password,
        )

        self.assertNotIn("GitHub", recovered_content)


if __name__ == "__main__":
    unittest.main()
