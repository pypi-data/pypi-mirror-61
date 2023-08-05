# -*- coding:utf-8 -*-

from itertools import permutations

from faker import Faker
from faker.providers import BaseProvider


class _Provider(BaseProvider):
    first_last_full = ["{{first_name}}", "{{last_name}}"]
    first_last_init = first_last_full + ["{{random_letter}}"]
    prefixes = ["_".join(perm) for perm in permutations(first_last_full)]
    prefixes += [".".join(perm) for perm in permutations(first_last_full)]
    prefixes += ["".join(perm) for perm in permutations(first_last_init, 2)]
    suffixes = ["", "{{year}}", "#", "##", "###", "####", "#####"]
    username_formats = []
    for prefix in prefixes:
        for suffixes in suffixes:
            username_formats.append(prefix + suffixes)

    safe_email_tlds = ("org", "com", "net")

    def domain(self) -> str:
        return f"example.{self.random_element(self.safe_email_tlds)}"

    def username(self) -> str:
        pattern = self.random_element(self.username_formats)
        username = self.numerify(self.generator.parse(pattern)).lower()
        return username


fake = Faker()
fake.add_provider(_Provider)


def domain() -> str:
    return fake.domain()


def username() -> str:
    return fake.username()
