from typing import Optional

import binascii
import hashlib
import os


def hash(password: Optional[str]) -> Optional[str]:
    if password is None:
        return None
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def hash_ha1(
    username: Optional[str], realm: Optional[str], password: Optional[str]
) -> Optional[str]:
    if username is None or realm is None or password is None:
        return None
    password_ha1 = "%s:%s:%s" % (username, realm, password)
    return hashlib.md5(password_ha1.encode('utf-8')).hexdigest()


def verify(stored_password: str, provided_password: str) -> bool:
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000
    )
    pwdhash_str = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash_str == stored_password
