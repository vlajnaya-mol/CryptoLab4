from MillerRabin import *
import math, random, os, hashlib, numpy

def get_e(euler):
    e = random.randint(2, euler)
    while math.gcd(euler, e) != 1:
        e = random.randint(2, euler)
    return e

def bxor_numpy(b1, b2):
    n_b1 = numpy.fromstring(b1, dtype='uint8')
    n_b2 = numpy.fromstring(b2, dtype='uint8')

    return (n_b1 ^ n_b2).tostring()

def hash_func(bytes, nbits):
    m = hashlib.sha256()
    m.update(bytes)
    h = m.digest()
    while len(h) < nbits // 8:
        m = hashlib.sha256()
        m.update(h)
        h += m.digest()
    return h[:nbits//8]
    
class RSA_OAEP():
    def __init__(self, prime_bits, m=256, k0=64, k1=192):
        self.prime_bits = prime_bits
        self.n = m + k0 + k1
        self.m = m
        self.k0 = k0
        self.k1 = k1
    
    def gen_key(self):
        p, q = gen_prime(self.prime_bits), gen_prime(self.prime_bits)
        N = p * q
        euler = (p - 1) * (q - 1)
        e = get_e(euler)
        d = mul_inv(e, euler)
        return (N, e), (N, d, p, q)
    
    def _encrypt(self, m, pbk):
        N, e = pbk
        assert m < N, f"m ({m}) must be lower than N ({N})"
        return pow(m, e, N)
    
    def _decrypt(self, c, sk):
        N, d, p, q = sk
        r1 = pow(c % p, d % (p - 1), p)
        r2 = pow(c % q, d % (q - 1), q)
        x1 = r1
        x2 = (r2 - x1) * mul_inv(p, q) % q
        m = x1 + x2 * p
        return m
    
    def H(self, bytes):
        return hash_func(bytes, self.k0)

    def G(self, bytes):
        return hash_func(bytes + b'\x01', self.m + self.k1)
    
    def encrypt_bytes(self, bytes, pbk):
        assert len(bytes) == self.m // 8
        bytes += b'\x00'*(self.k1 // 8)
        
        r = os.urandom(self.k0//8)
        bytes = bxor_numpy(bytes, self.G(r))
#         print(G(r))
        bytes = bytes + bxor_numpy(self.H(bytes), r)
        
        return self._encrypt(bytes_to_int(bytes), pbk)
    
    def decrypt_bytes(self, c, sk):
        c = int_to_bytes(self._decrypt(c, sk))
        X = c[:(self.m+self.k1)//8]
        r = bxor_numpy(self.H(X), c[-(self.k0//8):])
        m0 = bxor_numpy(X, self.G(r))
        m = m0[:self.m//8]
        return m
    