from pwdlib.hashers.argon2 import Argon2Hasher

from auth_service.src.domain.ports.password_ports import PasswordHashingPort


class Argon2PasswordHasher(PasswordHashingPort):
    def __init__(self, rounds: int = 18):
        self.crypt_context = Argon2Hasher(time_cost=rounds)

    def hash_password(self, password: str) -> str:
        self.crypt_context.identify
        return self.crypt_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.crypt_context.verify(plain_password, hashed_password)
