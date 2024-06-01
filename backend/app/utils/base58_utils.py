import base58


def int_to_str(num: int, prefix: str = "", seperator="_") -> str:
    """Return the ID as a string."""
    if num < 0:
        return ""
    base58_str = base58.b58encode_int(num).decode("utf-8")
    if not prefix:
        return base58_str
    else:
        return f"{prefix}{seperator}{base58_str}"


def str_to_int(base58_str: str, seperator="_") -> int:
    """Return the ID as an integer."""
    if not base58_str:
        return -1
    try:
        base58_str = base58_str.split(seperator)[-1]
        return base58.b58decode_int(base58_str)
    except ValueError:
        return -1
