# Emgen 📧
[![Versioning: CalVer](https://img.shields.io/badge/calver-YYYY.MM.DD.MICRO-22bfda.svg)](https://calver.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/github/license/etedor/emgen.svg)](https://github.com/etedor/emgen/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/emgen.svg)](https://pypi.org/project/emgen/)

**Emgen** generates random email addresses.

[![asciicast](https://etedor.github.io/emgen/README-demo.gif)](https://asciinema.org/a/Fk03dQR4GaQhOElBjl8VS8Qz6)

## Installation
Emgen is available on [PyPI](https://pypi.org/project/emgen/) and is installable with [pip](https://pip.pypa.io/en/stable/installing/):
```
$ pip3 install --user emgen
```

## Usage
Generate a random email address:
```
$ emgen
mt1ivirn@example.com
```

Generate an email address for your domain `corgi.example`:
```
$ emgen --domain corgi.example
aiemil8u@corgi.example
```

Generate a long email address for your domain `dane.example`:
```
$ emgen -d dane.example --length 16
vqjo0h8y4z2dgetd@dane.example
```

Make an alias to generate an address and copy it to your clipboard:
```
$ alias em="emgen -d greyhound.example -l12 --clipboard"
$ em
yx4su4olx2uq@greyhound.example
$ # display the contents of your clipboard:
$ xclip -sel clip -o
yx4su4olx2uq@greyhound.example
```

### Subaddressing
Emgen can generate random tags if your email provider supports [subaddressing](https://tools.ietf.org/html/rfc5233), such as [FastMail's](https://www.fastmail.com/help/receive/addressing.html)  or [Gmail's](https://gmail.googleblog.com/2008/03/2-hidden-ways-to-get-more-from-your.html) plus addressing.

Generate a tag for your Gmail account `john.doe84`:
```
$ emgen -d gmail.example --username john.doe84
john.doe84+7usnoxla@gmail.example
```

## License

Emgen is released under the [MIT License](https://opensource.org/licenses/MIT).
