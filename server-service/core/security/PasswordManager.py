import base64
import os
import hashlib
import hmac


class PasswordManager:
    __salt_len = 64

    @classmethod
    def hashing(cls, password: str) -> bytes:
        salt = os.urandom(64)
        password_hash = hashlib.pbkdf2_hmac('sha512', password.encode(), salt, 100005)
        return base64.encodebytes(salt + password_hash)

    @classmethod
    def verification(cls, password_hash: bytes, password: bytes) -> bool:
        password_hash = base64.decodebytes(password_hash)
        return hmac.compare_digest(
            password_hash[cls.__salt_len:],
            hashlib.pbkdf2_hmac('sha512', password, password_hash[0:cls.__salt_len], 100005)
        )
