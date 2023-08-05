# -*- coding:utf-8 -*-

import secrets
import string

CHARS = string.digits + string.ascii_lowercase


def localpart(length: int = 8) -> str:
    """Generate a random email address local-part.

    Local-parts are generated using a minimal set of the characters specified
    in RFC 5322.

    Args:
        length (int, optional): Length of the local-part (from 1 to 64).
            Defaults to 8.

    Returns:
        str: A randomly generated email address local-part.

    See Also:
        https://tools.ietf.org/html/rfc5322#section-3.4.1
        https://www.jochentopf.com/email/address.html

    """
    if not 1 <= length <= 64:
        raise ValueError(f"invalid value for `length`: {length}")
    lp = "".join(secrets.choice(CHARS) for _ in range(length))
    return lp
