
import base64
import json
import os
import tempfile

from pathlib import Path

from exceptions import VaultCorruptedError, VaultNotFoundError


VAULT_PATH = Path(__file__).resolve().parent / "vault.json"


def encode_bytes(data: bytes) -> str:
    """Encode bytes as a Base64 string."""

    return base64.b64encode(data).decode("utf-8")


def decode_bytes(data: str) -> bytes:
    """Decode a Base64 string into bytes."""

    return base64.b64decode(data, validate=True)


def build_vault_data(
    salt: bytes,
    nonce: bytes,
    ciphertext: bytes,
) -> dict:
    """Build the structure stored in the vault file."""

    return {
        "version": 1,
        "algorithm": "AES-256-GCM",
        "kdf": "Argon2id",
        "salt": encode_bytes(salt),
        "nonce": encode_bytes(nonce),
        "ciphertext": encode_bytes(ciphertext),
    }


def save_vault(vault_data: dict) -> None:
    """Save vault data using an atomic file replacement."""

    VAULT_PATH.parent.mkdir(parents=True, exist_ok=True)

    json_data = json.dumps(vault_data, indent=4)

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=VAULT_PATH.parent,
        delete=False,
    ) as temp_file:
        temp_file.write(json_data)
        temp_path = Path(temp_file.name)

    try:
        os.replace(temp_path, VAULT_PATH)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def load_vault() -> dict:
    """Load and validate the vault file."""

    if not VAULT_PATH.exists():
        raise VaultNotFoundError("Vault file was not found.")

    try:
        vault_data = json.loads(
            VAULT_PATH.read_text(encoding="utf-8")
        )

        required_fields = {
            "version",
            "algorithm",
            "kdf",
            "salt",
            "nonce",
            "ciphertext",
        }

        if not required_fields.issubset(vault_data):
            raise VaultCorruptedError(
                "Vault file is missing required fields."
            )

        if vault_data["version"] != 1:
            raise VaultCorruptedError(
                "Unsupported vault file version."
            )

        return vault_data

    except (json.JSONDecodeError, OSError, TypeError) as error:
        raise VaultCorruptedError(
            "Could not read the vault file."
        ) from error
