# coding: utf8
from Crypto.Cipher import AES
import base64


BS = AES.block_size


def __pad(s):
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


def __un_pad(s):
    return s[0:-ord(s[-1])]


# str不是16的倍数那就补足为16的倍数
def __add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)


# 加密
def encrypt(key, text):
    aes = AES.new(__add_to_16(key), AES.MODE_ECB)
    cipher_text = aes.encrypt(__add_to_16(__pad(text)))
    encrypted_text = str(base64.encodebytes(cipher_text), encoding='utf-8').replace('\n', '')
    return encrypted_text


# 解密
def decrypt(key, text):
    aes = AES.new(__add_to_16(key), AES.MODE_ECB)
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
    plain_text = aes.decrypt(base64_decrypted)
    decrypted_text = __un_pad(plain_text.decode('utf-8'))
    decrypted_code = decrypted_text.rstrip('\0')
    return decrypted_code


if __name__ == '__main__':
    k = "630AB742D8A54463"
    e = encrypt(k, "hello world")
    d = decrypt(k, e)
    print("加密:", e)
    print("解密:", d)