import numpy as np

cypher = [173, 0, 192, 159, 22, 23, 236, 37, 37, 31, 18, 226, 127, 159, 55, 83, 18, 186, 141, 56, 96, 20, 27, 49, 142, 19, 226, 86, 10, 26, 37, 185, 128, 115, 138, 96]
key = "eclipsky"

def rc4(key, data):
    S = list(range(256))
    j = 0
    out = []

    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append((char.item() - S[(S[i] + S[j]) % 256])%256)

    return out

res = rc4(key.encode(), np.array(cypher))
mat_inv = np.array(
    [
        [167, 214, 99, 125, 29, 213],
        [180, 50, 35, 197, 253, 150],
        [203, 84, 50, 206, 152, 150],
        [199, 243, 73, 104, 234, 69],
        [163, 84, 170, 216, 107, 189],
        [127, 219, 196, 158, 221, 222],
    ]
)

mat = (np.matmul(np.array(res).reshape((6,6)),mat_inv)%256).reshape(-1)

flag = "ACTF{"
kernel = [11,4,5,14]
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_@{}"
for i in range(2,36):
    for c in chars:
        tmp = flag + c
        if sum([ord(tmp[i+j])*kernel[j] for j in range(4)])%256 == mat[i]:
            flag = tmp
            break
    if c == "}":
        break
print(flag)