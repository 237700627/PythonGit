import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


def encrypt(pub_key_text, text):
    pub_key_text = '-----BEGIN PUBLIC KEY-----\n{}\n-----END PUBLIC KEY-----'.format(pub_key_text)
    rsakey = RSA.importKey(pub_key_text)
    cipher = PKCS1_v1_5.new(rsakey)
    cipher_text = cipher.encrypt(text.encode('utf-8'))
    cipher_text = base64.b64encode(cipher_text)
    return cipher_text.decode('utf-8')


def decrypt(pri_key_text, cipher_text):
    return ''


if __name__ == '__main__':
    _pri_key_text = 'MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAKc3Zsm+UxckhRdbDTQJI7ZBbJBWqlrgtd2AhQJ1bWyFhIcYuUPPLnTjy8P2WvXDokxvUuN8A+BkXVox3QxEALcw1WyLVLq6nAGciPsmiSLHAbXQaIkqH5q7+abDO7aWsqPUOBmjepCTrHv9oMUzPTjZ5yKVZdQwhIx+81tB4mNlAgMBAAECgYA/TV/iO+Tku/SOdO+4pUUZuAbLVaPEJ5FxuzefSKkWDi2vnxJzszkZEyuOkfK5W0hTu0kbyVUGW7hjbsEJ5ayHEGUuGUzRVIYLAr8u5s92I7qqLteJRm5qXye6/V/nJbv4dhHa+m59/5W4inA08mIAobmE+qY6mSM5U91vgqBPOQJBANk3TKpwplbBrCQGLol9GSg0bF8H22EoHZyR/qoezscZTsApc6CvDud6CkbrkpiuJH3K0D16I5Ard7AeWAi8ZacCQQDFEq0h+FapZ83g6SQX1Rz3I9FsknluALSEMbXfQjYm8XMawswagxup+J5UM1DUpE3rNHWhdTi7nG9kdkEx7WgTAkBtj5b74RYFbGqHQRb4AkFOJiMDS9M7jiBheMIazK8/fWRbSI0p3yKFXukQHII0wKFnUYT3fUOy1Dnqe2OsBFrBAkEAg7GWVvQQXYaLsve5cd+tSo35/hbn5JW+C/T4N6iUbXO+WqzAHhttGimVDGl6Y48krr/Qt8OQ1PaWDclkicu/VwJAFa0vn6dBZnHlUBTGS0qSQiDbhurxX8XEmT3KgzH5kBe0XHNhFy2veWtjULZmvfjkNzdHak6JUa+kbEWxzdBfSw=='
    _pub_key_text = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCnN2bJvlMXJIUXWw00CSO2QWyQVqpa4LXdgIUCdW1shYSHGLlDzy5048vD9lr1w6JMb1LjfAPgZF1aMd0MRAC3MNVsi1S6upwBnIj7JokixwG10GiJKh+au/mmwzu2lrKj1DgZo3qQk6x7/aDFMz042ecilWXUMISMfvNbQeJjZQIDAQAB'

    _encrypt_text = encrypt(_pub_key_text, '123456')
    print('加密：', _encrypt_text)
    _plain_text = decrypt(_pri_key_text, _encrypt_text)
    print('解密：', _plain_text)