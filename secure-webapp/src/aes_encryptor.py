import base64
import os
from Crypto.Cipher import AES


def key_encode_to_base64(key):
    return base64.b64encode(key).decode('utf-8')

def encryptor(message, key=os.urandom(16)):
    cipher = AES.new(key, AES.MODE_CBC)
    block_size = AES.block_size
    message_bytes = message.encode('utf-8')
    padding_bytes = block_size - len(message_bytes) % block_size
    padded_bytes = message_bytes + padding_bytes * bytes([padding_bytes])
    iv = cipher.iv
    encrypted_bytes = cipher.encrypt(padded_bytes)
    key_str = key_encode_to_base64(key)
    iv_str = base64.b64encode(iv).decode('utf-8')
    encrypted_str = base64.b64encode(encrypted_bytes).decode('utf-8')
        
    return {'key':key_str,'iv':iv_str,'encrypted':encrypted_str}


# key = os.urandom(16)
# print(encrypt_message('hello world !',key))
# print(encrypt_message('This is !', key))
# print(encrypt_message('Shit !', key))
