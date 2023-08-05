# -*- coding:utf-8 -*-

import random

from email_validator import EmailNotValidError, validate_email

from emgen.common import fake
from emgen.core import local_part


def _is_valid(addr):
    try:
        validate_email(addr)
        return True
    except EmailNotValidError:
        return False


def test_local_part(trials: int = 99_999) -> None:
    """Test generation of random email address local-parts.

    Args:
        trials (int, optional): Number of tests to perform. Defaults to 99_999.

    """
    for _ in range(trials):
        length = random.randint(4, 64)
        username = random.choice([fake.username(), None])
        separator = random.choice("-+")
        local = local_part(
            length=length, username=username, separator=separator
        )
        domain = fake.domain()

        addr = f"{local}@{domain}"
        assert _is_valid(addr)
