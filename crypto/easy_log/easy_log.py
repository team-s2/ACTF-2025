from Crypto.Util.number import long_to_bytes, bytes_to_long, isPrime
from os import urandom
from random import randint
from collections import namedtuple
from signal import alarm

Point = namedtuple("Point", "x y")
O = "Origin"

def point_addition(P, Q, n):
	if P == O:
		return Q
	if Q == O:
		return P
	x = (P.x * Q.y + P.y * Q.x - P.x * Q.x) % n
	y = (P.x * Q.x + P.y * Q.y) % n
	return Point(x, y)
	
def double_and_add(k, P, n):
	Q = P
	R = O
	while(k > 0):
		if k & 1:
			R = point_addition(R, Q, n)
		k >>= 1
		Q = point_addition(Q, Q, n)
	return R

with open("flag.txt", "rb") as f:
	flag = f.read()

assert len(flag) == 50
flag = urandom(randint(38, 48)) + flag
flag = flag + urandom(118 - len(flag))

flag1, flag2 = bytes_to_long(flag[:68]), bytes_to_long(flag[68:])

n = 0x231d5fa471913e79facfd95e9b874e2d499def420e0914fab5c9f87e71c2418d1194066bd8376aa8f02ef35c1926f73a46477cd4a88beae89ba575bb3e1b04271426c6706356dd8cd9aa742d7ad0343f8939bfd2110d45122929d29dc022da26551e1ed7000
G1 = Point(0xf22b9343408c5857048a19150c8fb9fd44c25d7f6decabc10bf46a2250a128f0df15adc7b82c70c0acaf855c0e898b141c9c94ba8aef8b67ea298c6d9fd870ea70e1c4f8a1b595d15373dc6db25a4ecddf626a64f47beba5538b7f733e4aa0c4f1fd4c291d, 0x8d3264514b7fdbce97fbaedb33120c7889a1af59691a1947c2c7061347c091b0950ca36efaa704514004a988b9b87b24f5cebf2d1c7bef44ff172519e1a62eb62cde234c94bd0ab39375d7ddb42e044090c8db46d3f965ef7e4753bc41dac3b8b3ae0cdb57)
G2 = Point(0x81919777837d3e5065c6f7f6801fe29544180be9db2137f075f53ebb3307f917183c6fc9cdfc5d75977f7, 0xd1a586d6848caa3a5436a86d903516d83808ce2fa49c5fb3f183ecb855e961c7e816a7ba8f588ef947f19)

f1 = double_and_add(flag1, G1, n)

print(f1)

alarm(30)

if flag1 != int(input()):
	exit()

p = int(input())

assert isPrime(p) and p.bit_length() == 400

f2 = double_and_add(flag2, G2, p)

print(f2)