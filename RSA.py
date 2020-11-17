from MillerRabin import *
import math, random


def get_e(euler):
    e = random.randint(2, euler)
    while math.gcd(euler, e) != 1:
        e = random.randint(2, euler)
    return e

class RSA():
    def __init__(self, prime_bits):
        self.prime_bits = prime_bits
    
    def gen_key(self):
        p, q = gen_prime(self.prime_bits), gen_prime(self.prime_bits)
        N = p * q
        euler = (p - 1) * (q - 1)
        e = get_e(euler)
        d = mul_inv(e, euler)
        return (N, e), (N, d, p, q)
    
    def encrypt(self, m, pbk):
        N, e = pbk
        assert m < N, f"m ({m}) must be lower than N ({N})"
        return pow(m, e, N)
    
    def decrypt(self, c, sk):
        N, d, p, q = sk
        r1 = pow(c % p, d % (p - 1), p)
        r2 = pow(c % q, d % (q - 1), q)
        x1 = r1
        x2 = (r2 - x1) * mul_inv(p, q) % q
        m = x1 + x2 * p
        return m
    
    def encrypt_bytes(self, bytes, pbk):
        return self.encrypt(bytes_to_int(bytes), pbk)
    
    def decrypt_bytes(self, c, sk):
        return int_to_bytes(self.decrypt(c, sk))
    