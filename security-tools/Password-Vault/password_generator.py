
import secrets
import string


def generate_password(length: int = 20) -> str:
    """Generate a secure password containing different character types."""

    if length < 4:
        raise ValueError("Password length must be at least 4.")

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{};:,.?"

    password_chars = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols),
    ]

    all_chars = lowercase + uppercase + digits + symbols

    password_chars.extend(
        secrets.choice(all_chars)
        for _ in range(length - 4)
    )

    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)
