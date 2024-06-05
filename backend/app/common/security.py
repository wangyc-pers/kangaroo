import secrets
import string
import uuid

import base58
import bcrypt


def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    """
    Checks if a password matches a hashed password.

    Args:
        password (str): The password to be checked.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    if isinstance(password, str):
        password = password.encode("utf-8")
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password, hashed_password)


def gen_random_string(
    length: int = 16, charsets: str = string.ascii_letters + string.digits
) -> str:
    """
    Generates a random string of specified length.

    Args:
        length (int): The length of the random string. Default is 16.
        charsets (str): The characters to choose from when generating the random string.
                        Default is a combination of ASCII letters and digits.

    Returns:
        str: The generated random string.
    """
    return "".join(secrets.choice(charsets) for _ in range(length))


def gen_unique_str(length: int = 22, prefix: str = None, sep="_") -> str:
    """
    Generate a unique string of specified length.

    Args:
        length (int): The length of the unique string. Default is 22.
        prefix (str): Optional prefix to be added to the unique string. Default is None.

    Returns:
        str: The generated unique string.
    """
    uid = uuid.uuid4()
    unique_str = base58.b58encode(uid.bytes).decode("utf-8")
    if len(unique_str) < length:
        charsets = base58.alphabet.decode("utf-8")
        unique_str += gen_random_string(length - len(unique_str), charsets)
        unique_str = unique_str[:length]
        
    if prefix:
        unique_str = f"{prefix}{sep}{unique_str}"

    return unique_str