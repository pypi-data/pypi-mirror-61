# -*- coding:utf-8 -*-

import secrets
from typing import Optional


def local_part(
    length: int = 8, username: Optional[str] = None, separator: str = "+"
) -> str:
    """Construct an email address local-part.

    Randomly generate a local-part using a safe subset of the allowable
    characters specified in RFC 5322.

    If a username is supplied (i.e., subaddressing is used), the random
    output will be used as the "detail" sub-part of the local-part. The
    detail sub-part will be truncated if the combined length of the username,
    separator, and detail sub-parts are greater than 64.

    Args:
        length (int, optional): Length of the generated local-part or detail
            sub-part (from 1 to 64). Defaults to 8.
        username (str, optional): The username sub-part of the local-part.
            Defaults to None.
        separator (str, optional): Separator between the username and
            detail sub-parts. Defaults to "+".

    Returns:
        str: The constructed local-part.

    See Also:
        https://tools.ietf.org/html/rfc5322#section-3.4.1
        https://tools.ietf.org/html/rfc5233#section-1
        https://www.jochentopf.com/email/address.html

    """

    def _choice(length):
        chars = "0123456789abcdefghijklmnopqrstuvwxyz"
        return "".join(secrets.choice(chars) for _ in range(length))

    if username:
        combined = len(username + separator)
        if combined + length >= 64:
            length = 64 - combined
        detail = _choice(length)
        local = f"{username}{separator}{detail}"
    else:
        local = _choice(length)

    return local
