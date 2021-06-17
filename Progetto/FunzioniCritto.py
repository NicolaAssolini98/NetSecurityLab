import base64
from hashlib import sha256, sha1
import random
from Cryptodome.Cipher import AES


def pad(s):
    block_size = 16
    remainder = len(s) % block_size
    padding_needed = block_size - remainder
    return s + padding_needed * ' '


def unpad(s):
    return s.rstrip()


def get_public_key():
    p = 19
    g = 13
    a = random.randint(2, p - 1)

    return pow(g, a, p), a, p


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


def encode_msg(plain_text, msg_key, key, x=0):
    """
    metto tutta key perchè è più corta di 32B
    sha256_a = SHA256(msg_key + substr(key, x, 36));
    sha256_b = SHA256(substr(key, 40 + x, 36) + msg_key);
    """
    sha256_a = sha256(msg_key + (str(key)).encode()).digest()
    sha256_b = sha256(str(key).encode() + msg_key).digest()
    private_key = sha256_a[0:8] + sha256_b[8:24] + sha256_a[24:32]
    iv = sha256_b[0:4] + sha256_a[8:16] + sha256_b[24:28]
    padded_text = pad(plain_text)
    cipher_config = AES.new(private_key, AES.MODE_CBC, iv)

    return cipher_config.encrypt(padded_text.encode())



def decode_msg(enc, msg_key, key, x=0):
    """
    metto tutta key perchè è più corta di 32B
    sha256_a = SHA256(msg_key + substr(key, x, 36));
    sha256_b = SHA256(substr(key, 40 + x, 36) + msg_key);
    """
    sha256_a = sha256(msg_key + (str(key)).encode()).digest()
    sha256_b = sha256(str(key).encode() + msg_key).digest()
    aes_key = sha256_a[0:8] + sha256_b[8:24] + sha256_a[24:32]
    aes_iv = sha256_b[0:4] + sha256_a[8:16] + sha256_b[24:28]
    aes = AES.new(aes_key, AES.MODE_CBC, aes_iv)

    return unpad(aes.decrypt(enc))

