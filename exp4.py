import random
from typing import Tuple

class RSA:
    def __init__(self, key_size: int = 2048):
        self.key_size = key_size
        self.public_key, self.private_key = self._generate_keys()
        self.block_size = (key_size // 8) - 11

    @staticmethod
    def _is_prime(n: int, k: int = 5) -> bool:
        if n <= 1:
            return False
        elif n <= 3:
            return True
        elif n % 2 == 0:
            return False
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for __ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    @staticmethod
    def _generate_prime(bits: int) -> int:
        while True:
            p = random.getrandbits(bits)
            p |= (1 << bits - 1) | 1
            if RSA._is_prime(p):
                return p

    @staticmethod
    def _extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = RSA._extended_gcd(b % a, a)
            return g, x - (b // a) * y, y

    @staticmethod
    def _modinv(a: int, m: int) -> int:
        g, x, y = RSA._extended_gcd(a, m)
        if g != 1:
            raise ValueError('模逆元不存在。')
        else:
            return x % m

    def _generate_keys(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        p = self._generate_prime(self.key_size // 2)
        q = self._generate_prime(self.key_size // 2)
        while p == q:
            q = self._generate_prime(self.key_size // 2)
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537
        while True:
            try:
                d = self._modinv(e, phi)
                break
            except ValueError:
                e += 2
                if e >= phi:
                    p = self._generate_prime(self.key_size // 2)
                    q = self._generate_prime(self.key_size // 2)
                    n = p * q
                    phi = (p - 1) * (q - 1)
                    e = 65537
        return (n, e), (n, d)

    @staticmethod
    def _pkcs1_pad(data: bytes, block_size: int) -> bytes:
        if len(data) > block_size - 11:
            raise ValueError("数据过长，需要先分组。")
        padding_length = block_size - len(data) - 3
        padding = bytes([random.randint(1, 255) for _ in range(padding_length)])
        return b'\x00\x02' + padding + b'\x00' + data

    @staticmethod
    def _pkcs1_unpad(padded_data: bytes) -> bytes:
        if not padded_data.startswith(b'\x00\x02'):
            raise ValueError("无效的PKCS#1填充。")
        try:
            sep_index = padded_data.index(b'\x00', 2)
        except ValueError:
            raise ValueError("无效的PKCS#1填充。")
        return padded_data[sep_index+1:]

    def encrypt(self, plaintext: bytes, public_key: Tuple[int, int] = None) -> bytes:
        if public_key is None:
            public_key = self.public_key
        n, e = public_key
        max_block_size = (self.key_size // 8) - 11
        ciphertext = b''
        for i in range(0, len(plaintext), max_block_size):
            block = plaintext[i:i+max_block_size]
            padded_block = self._pkcs1_pad(block, (self.key_size // 8))
            m = int.from_bytes(padded_block, 'big')
            if m >= n:
                raise ValueError("填充后数据仍然过大。")
            c = pow(m, e, n)
            ciphertext += c.to_bytes(self.key_size // 8, 'big')
        return ciphertext

    def decrypt(self, ciphertext: bytes, private_key: Tuple[int, int] = None) -> bytes:
        if private_key is None:
            private_key = self.private_key
        n, d = private_key
        block_size = self.key_size // 8
        if len(ciphertext) % block_size != 0:
            raise ValueError("密文长度不正确。")
        plaintext = b''
        for i in range(0, len(ciphertext), block_size):
            block = ciphertext[i:i+block_size]
            c = int.from_bytes(block, 'big')
            m = pow(c, d, n)
            padded_block = m.to_bytes(block_size, 'big')
            try:
                plaintext += self._pkcs1_unpad(padded_block)
            except ValueError as e:
                raise ValueError("解密失败: 无效的填充。") from e
        return plaintext

if __name__ == "__main__":
    rsa = RSA(2048)
    print("公钥 (n, e):", rsa.public_key)
    print("\n私钥 (n, d):", rsa.private_key)
    message = b"Hello, RSA! This is a long message that will be split into blocks and padded."
    print("\n明文:", message.decode())
    encrypted = rsa.encrypt(message)
    print("\n密文 (HEX):", encrypted.hex())
    decrypted = rsa.decrypt(encrypted)
    print("\n解密所得:", decrypted.decode())
