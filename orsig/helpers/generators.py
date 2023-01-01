import secrets
import random


class Generator:

    @staticmethod
    def generate_hash():
        return secrets.token_hex(16)

    @staticmethod
    def generate_pk():
        return secrets.randbits(31)

    @staticmethod
    def hash_generate(value):
        def generate():
            return secrets.token_hex(value)

        return generate()

    @staticmethod
    def ref_generate():
        return secrets.token_hex(4)

    @staticmethod
    def generate_int():
        return secrets.choice(range(100000, 999999))
