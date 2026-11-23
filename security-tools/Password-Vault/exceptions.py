
class VaultError(Exception):
    """Base exception for vault-related errors."""


class VaultAlreadyExistsError(VaultError):
    """Raised when attempting to create an existing vault."""


class VaultNotFoundError(VaultError):
    """Raised when the vault file does not exist."""


class VaultCorruptedError(VaultError):
    """Raised when the vault file is invalid or corrupted."""
