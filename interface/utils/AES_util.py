# -*- coding:UTF-8 -*-
import  base64
from Crypto.Cipher import AES
import json

class Aes_utils():
    def __init__(self):
        self.bs = 16
        self.PADDING = lambda s: s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def encrypt(self,data,key):

        aes = AES.new(self.add_to_16(key), AES.MODE_ECB)
        encrypted_data = base64.b64encode(aes.encrypt(self.PADDING(data).encode())).decode().replace('\n', '')# 执行加密并转码返回bytes
        print(encrypted_data)
        return encrypted_data

    # str不是16的倍数那就补足为16的倍数
    def add_to_16(self,value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)

    def decrypt(self,data,aeskey):
        aes = AES.new(self.add_to_16(aeskey), AES.MODE_ECB)
        base64_decrypted = base64.b64decode(data.encode(encoding='utf-8'))
        decrypted_text = str(aes.decrypt(base64_decrypted).decode()).replace('\0', '')
        print('解密后的数据为：',decrypted_text)
        return decrypted_text
    
if __name__ == "__main__":
    data = '{"pageNum":1,"pageSize":10,"taskStatus":"01"}'
    key = '2E185C92EFFC9BFF'
    
    a= Aes_utils()
    b = a.encrypt(data,key)
    print(b)
