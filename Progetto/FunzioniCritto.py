from hashlib import sha256, sha1
import random


def get_public_key():
    p = 19
    g = 13
    a = random.randint(2, p - 1)

    return pow(g, a, p), a, p


def encode_msg(payload):
    return 0


def get_fingerprint(key):
    long_fp = sha1(str(key).encode()).hexdigest()
    return long_fp[-16:]  # last 64 bits


def get_msg_key(plaintext, key, x=0):
    """
    metto tutta key perchè è più corta di 32B
    SHA256 (substr (key, 88+x, 32) + plaintext + random_padding);
    """
    key_b = str(key).encode()
    plaintext_b = plaintext.encode()
    msg_key_large = sha256(key_b + plaintext_b).hexdigest()
    return msg_key_large[16:48]


'''
 sha256_a = SHA256(msg_key + substr(key, x, 36));
    sha256_b = SHA256(substr(key, 40 + x, 36) + msg_key);
    aes_key = substr(sha256_a, 0, 8) + substr(sha256_b, 8, 16) + substr(sha256_a, 24, 8);
    aes_iv = substr(sha256_b, 0, 8) + substr(sha256_a, 8, 16) + substr(sha256_b, 24, 8);
'''
