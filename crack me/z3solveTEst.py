from z3 import *

s = Solver()

x = BitVec("x", 8)
y = BitVec("y", 8)
z = BitVec("z", 8)
t = BitVec("t", 8)
k = BitVec("k", 8)

s.add(x ^ t == 88 ^ 0x50)
s.add(x ^ y ^ k == 124)
s.add(x ^ y ^ z == 123)
s.add(x ^ y ^ z ^ t == 24)
s.add(y ^ z ^ k ^ t == 7)

s.check()

print(s.model())