import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def aes_encrypt(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(plaintext, AES.block_size))

def aes_decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)

plaintext = binascii.unhexlify("7c7feef136db0d41fdd4c3c7c8a19cea4af5b1ff07b56d2ecc039e6cfc87dc03d496a2e4d851a27335ab44195e04010d7f1a7c5c06618a95364f1bb7cc873359e0ee8f26111d75ab61e7d3a0ecba21418b3a9c30cfb56ea0a64ab9aecb24c9afc755c34e")
key = binascii.unhexlify("d078936926b3ee13abaf32fb8895ef80")
iv = binascii.unhexlify("dc5f7b8d416f05fbe3fbf2d3e9215738")

ciphertext = aes_encrypt(plaintext, key, iv)
print("密文:", binascii.hexlify(ciphertext).decode())

decrypted = aes_decrypt(ciphertext, key, iv)
if decrypted == plaintext:
    print("解密验证成功！")
else:
    print("解密验证失败！")
