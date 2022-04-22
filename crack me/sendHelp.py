from z3 import *

s = Solver()

a = BitVec("a", 8 * 1337) # 253
b = BitVec("b", 8 * 1337) # 18
c = BitVec("c", 8 * 1337) #34

s.add(a ^ b ^ c == 253 ^ 18 ^ 34)
s.add(b ^ c == 48)
s.add(c ^ a == 223 )



s.add(a < 0xff, a > 0, b < 0xff,  c < 0xff)

print(s.check())
print(s.model())