import base64
import hashlib


def encode_pw(username, password):
    initialHash = hashlib.sha256((password + username.lower()).encode('utf8')).digest()
    hashInBase64 = base64.b64encode(initialHash).decode('utf8')
    return hashInBase64
