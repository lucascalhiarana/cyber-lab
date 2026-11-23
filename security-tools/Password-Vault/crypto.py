
import secrets

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32

ARGON2_TIME_COST = 3
ARGON2_MEMORY_COST = 65536
ARGON2_PARALLELISM = 4


def generate_salt() -> bytes:
    """Generate a cryptographically secure random salt."""

    return secrets.token_bytes(SALT_SIZE)


def derive_key(master_password: str, salt: bytes) -> bytes:
    """Derive an encryption key from the master password."""

    return hash_secret_raw(
        secret=master_password.encode("utf-8"),
        salt=salt,
        time_cost=ARGON2_TIME_COST,
        memory_cost=ARGON2_MEMORY_COST,
        parallelism=ARGON2_PARALLELISM,
        hash_len=KEY_SIZE,
        type=Type.ID,
    )


def encrypt_data(data: bytes, key: bytes) -> tuple[bytes, bytes]:
    """Encrypt data using AES-256-GCM."""

    nonce = secrets.token_bytes(NONCE_SIZE)
    aesgcm = AESGCM(key)

    ciphertext = aesgcm.encrypt(nonce, data, None)

    return nonce, ciphertext


def decrypt_data(
    nonce: bytes,
    ciphertext: bytes,
    key: bytes,
) -> bytes:
    """Decrypt and authenticate data using AES-GCM."""

    aesgcm = AESGCM(key)

    return aesgcm.decrypt(nonce, ciphertext, None)
