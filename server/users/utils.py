from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
import base64
import os


def encrypt_token(value):
    SECRET_KEY = b'MySuperSecretKeyForParamsToken12'  # Must be 32 bytes for AES-256


    iv = os.urandom(16)
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    padded_data = pad(json.dumps(value).encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    data = {
        "iv": base64.b64encode(iv).decode("utf-8"),
        "value": base64.b64encode(encrypted_data).decode("utf-8"),
        }
    json_data = json.dumps(data)
    return base64.b64encode(json_data.encode()).decode("utf-8")
