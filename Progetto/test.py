import base64

from FunzioniCritto import *

key = 7
msg_key = get_msg_key("ciao", key)
en = encode_msg("ciao", msg_key.encode(), key)



decrypted = decode_msg(en, msg_key.encode(), key)
print(bytes.decode(decrypted))

# AES 256 encryption/decryption using pycrypto library
