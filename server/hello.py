from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json
import base64

def decrypt_token(encrypted_token):
    SECRET_KEY = b'MySuperSecretKeyForParamsToken12'  # Must be 32 bytes for AES-256

    # Decode the base64 encoded token
    json_data = base64.b64decode(encrypted_token).decode("utf-8")
    data = json.loads(json_data)

    # Extract the IV and encrypted value
    iv = base64.b64decode(data["iv"])
    encrypted_data = base64.b64decode(data["value"])

    # Create a new AES cipher with the same secret key and IV
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)

    # Decrypt and unpad the data
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    decrypted_json = json.loads(decrypted_data.decode("utf-8"))

    return decrypted_json

# Example usage:
encrypted_token = "eyJpdiI6ICI2OHN3YWlRR1ZQSmR4SFhlckswRXhRPT0iLCAidmFsdWUiOiAiVjZyS0NxWDRiVEplRHlCOGV5SUlXSDdYc0NCaCtLUm5yaTJibkp6cnZjNkJZcWVYV21NK2h4a0dMT3BnaXNpVFNnalh0WktyVDVsb1dkMmI2SVlNb3dZY0Nud0RTKzNlQnptUjE2TDNkUVVxbDR5R2ZwV0hzTXdBWnl3RDJiYUpuRVQxY0EwWHJYSkgwQlpKMUMxRUtmQVRERGlIRjFNWGxGQzltZHBaeHNwKzhqY2REVHEwRFNZM1c5WmVIT1JvIn0="
decrypted_data = decrypt_token(encrypted_token)
print(decrypted_data)