# -*- coding:utf-8 -*-

import string

from emgen.core import localpart

CHARS = string.digits + string.ascii_lowercase


def test_localpart(trials: int = 99_999, length: int = 8) -> None:
    """Test generation of random email address local-parts.

    Args:
        trials (int, optional): Number of tests to perform. Defaults to 99_999.
        length (int, optional): Length of the local-part (from 1 to 64).
            Defaults to 8.

    """
    for _ in range(trials):
        lp = localpart(length=length)
        len_lp = len(lp)

        assert len_lp == length
        assert 1 <= len_lp <= 64
        assert set(lp) <= set(CHARS)
