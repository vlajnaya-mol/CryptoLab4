import random, math

def miller_rabin(n, k=6):
    if n == 2:
        return True
    if n % 2 == 0 or n == 1:
        return False

    m = n - 1
    s = 0
    while m % 2 == 0:
        m = m // 2
        s += 1
    for i in range(k):
        a = random.randint(2, n - 1)
        b = pow(a, m, n)
        if b == 1 or b == n - 1:
            continue
        
        for i in range(s - 1):
            b = pow(b, 2, n)
            if b == n - 1:
                return True
        else:
            return False
        
    return True

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: 
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1

def gen_prime(n_bits):
    modulo = 2 ** n_bits
    p = random.randint(modulo//2, modulo-1)
    while not miller_rabin(p, 7):
        p = random.randint(modulo//2, modulo-1)
    return p

def bytes_to_int(bytes):
    return int.from_bytes(bytes, 'big')

def byte_length(n):
    return math.ceil(n.bit_length() / 8)

def int_to_bytes(n, fill_size=-1):
    bytes_required = fill_size if fill_size != -1 else byte_length(n)
    return n.to_bytes(bytes_required, 'big')