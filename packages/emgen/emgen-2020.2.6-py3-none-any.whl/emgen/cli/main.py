#!/usr/bin/env python3

import argparse
import sys
import textwrap

import pyperclip
from email_validator import EmailNotValidError, validate_email

from emgen import __version__
from emgen.core import local_part


def _has_clipboard():
    try:
        orig = pyperclip.paste()
        pyperclip.copy(orig)
        return True
    except pyperclip.PyperclipException:
        return False


def main():
    has_clipboard = _has_clipboard()

    parser = argparse.ArgumentParser(
        prog="emgen",
        description="Generate random email addresses.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-c",
        "--clipboard",
        action="store_true",
        default=False,
        help="copy addr to clipboard (default: %(default)s)"
        if has_clipboard
        else argparse.SUPPRESS,
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    address_description = textwrap.dedent(
        f"""\
        Email addresses are made up of a local-part, "@", and a domain name.
        The local-part will be filled randomly with LENGTH characters.

        examples:
            emgen
            {local_part()}@example.com

            emgen --domain corgi.example
            {local_part()}@corgi.example

            emgen -d dane.example --length 16
            {local_part(length=16)}@dane.example
        """
    )
    address_group = parser.add_argument_group(
        "address arguments", address_description
    )
    address_group.add_argument(
        "-d",
        "--domain",
        default="example.com",
        type=str,
        help="domain name (default: %(default)s)",
        metavar="DOMAIN",
        dest="domain",
    )
    address_group.add_argument(
        "-l",
        "--length",
        default=8,
        type=int,
        help=textwrap.dedent(
            """\
            length of the generated local-part or detail
            (default: %(default)s, range: 1 to 64)
            """
        ),
        metavar="LENGTH",
        dest="length",
    )

    subaddress_description = textwrap.dedent(
        f"""\
        If a USERNAME is supplied, the local-part will be split into two
        sub-parts - username and detail - joined by "+" or the supplied
        SEPARATOR.

        The detail will be filled randomly with LENGTH characters. However,
        the combined length of the local-part, including username, separator,
        and detail, is still limited to 64 characters.

        example:
            emgen -d gmail.example --username john.doe84
            john.doe84+{local_part()}@gmail.example
        """
    )
    subaddress_group = parser.add_argument_group(
        "subaddress arguments", subaddress_description
    )
    subaddress_group.add_argument(
        "-u",
        "--username",
        default=None,
        type=str,
        help="username to prepend to the addr (default: %(default)s)",
        metavar="USERNAME",
    )
    subaddress_group.add_argument(
        "-s",
        "--separator",
        default="+",
        type=str,
        help='separator between the username and detail (default: "%(default)s")',
        metavar="SEPARATOR",
    )

    args = parser.parse_args()

    local = local_part(args.length, args.username, args.separator)
    addr = f"{local}@{args.domain}"

    try:
        validate_email(addr)
    except EmailNotValidError as e:
        message = str(e).lower().rstrip(".")
        print("error:", message)
        sys.exit(1)

    if args.clipboard:
        if has_clipboard:
            pyperclip.copy(addr)
        else:
            warning = "warning: could not find a clipboard for your system"
            print(warning, file=sys.stderr)

    print(addr)
