from z3 import *

key = 0xf0

def encrypt(flagEncrypt):

	#f = open("thisis.txt", "w")

	#flagEncrypt = [0x6b, 0x63, 0x73, 0x63, 0x74, 0x72, 0x61, 0x69, 0x6e, 0x69, 0x6e, 0x67, 0x7b, 0x6d, 0x61, 0x6b, 0x65, 0x6d, 0x65, 0x61, 0x67, 0x72, 0x65, 0x61, 0x74, 0x6d, 0x61, 0x6e, 0x7d]
	#flagEncrypt = [107, 99, 115, 99, 116, 114, 97, 105, 110, 105, 110, 103, 123, 109, 97, 107, 101, 109, 101, 97, 103, 114, 101, 97, 116, 109, 97, 110, 125]
	#flagEncrypt = [0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 1, 3, 0x2d, 0x0c, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0x0a, 0x44, 0x24, 0x2c]

	flag2 = []

	for i in range(len(flagEncrypt)):
		flag2.append(1)

	for i in range(0, len(flagEncrypt)):
		flag2[i] = flagEncrypt[i]

	#flag2[i] ^= key

	last = key
	for i in range(0, 0x539):
		#print(flagEncrypt)
		for j in range(0, len(flagEncrypt)):
			if(j == 0):
				flag2[j] ^= last
			else:
				flag2[j] ^= flagEncrypt[j - 1]

		last = flagEncrypt[len(flagEncrypt) - 1]

		for b in range(0, len(flagEncrypt)):
			flagEncrypt[b] = flag2[b]

	#print(flagEncrypt)


def decrypt():

#  0        2                    7   8    9      11        13      15   16                 21
#  0,       2,                   7,  8,   9,     11,       13,     15,  16,                21,
# [72, 50, 40, 115, 71, 94, 75, 114, 37, 84, 55, 6,   89, 110, 45, 21,  89, 31, 14, 10, 6, 59]
# [56, 50, 88, 115, 71, 94, 75, 2,   85, 36, 55, 118, 89, 30,  45, 101, 41, 31, 14, 10, 6, 75]
	s = Solver()
	target = [0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 1, 3, 0x2d, 0x0c, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0x0a, 0x44, 0x24, 0x2c]
	#target =  [72, 95, 54, 53, 53, 37, 20, 44, 29, 1, 3, 45, 12, 111, 53, 97, 126, 52, 10, 68, 36, 44]

	v = [BitVec("v%i"%i, 8 * 21) for i in range(len(target))]

	s.add(target[0] == key ^   v[1]^v[6]^v[7]^v[9]^v[11]^v[13]^v[14]^v[15]^v[20]                  )
	s.add(target[1] ==   	   v[0]^v[2]^v[7]^v[8]^v[10]^v[12]^v[14]^v[15]^v[16]^v[21]                   )
	s.add(target[2] == key ^   v[0]^v[1]^v[3]^v[8]^v[9]^v[11]^v[13]^v[15]^v[16]^v[17]               )
	s.add(target[3] ==         v[0]^v[1]^v[2]^v[4]^v[9]^v[10]^v[12]^v[14]^v[16]^v[17]^v[18]         )
	s.add(target[4] ==         v[1]^v[2]^v[3]^v[5]^v[10]^v[11]^v[13]^v[15]^v[17]^v[18]^v[19]               )
	s.add(target[5] ==         v[2]^v[3]^v[4]^v[6]^v[11]^v[12]^v[14]^v[16]^v[18]^v[19]^v[20]         )
	s.add(target[6] ==         v[3]^v[4]^v[5]^v[7]^v[12]^v[13]^v[15]^v[17]^v[19]^v[20]^v[21]        )
	s.add(target[7] == key ^   v[0]^v[4]^v[5]^v[6]^v[8]^v[13]^v[14]^v[16]^v[18]^v[20]^v[21]                    )
	s.add(target[8] == key ^   v[1]^v[5]^v[6]^v[7]^v[9]^v[14]^v[15]^v[17]^v[19]^v[21]              )
	s.add(target[9] == key ^   v[2]^v[6]^v[7]^v[8]^v[10]^v[15]^v[16]^v[18]^v[20]                   )
	s.add(target[10] ==        v[0]^v[3]^v[7]^v[8]^v[9]^v[11]^v[16]^v[17]^v[19]^v[21]                    )
	s.add(target[11] == key ^  v[0]^v[1]^v[4]^v[8]^v[9]^v[10]^v[12]^v[17]^v[18]^v[20]                   )
	s.add(target[12] ==        v[0]^v[1]^v[2]^v[5]^v[9]^v[10]^v[11]^v[13]^v[18]^v[19]^v[21]      )
	s.add(target[13] == key ^  v[0]^v[1]^v[2]^v[3]^v[6]^v[10]^v[11]^v[12]^v[14]^v[19]^v[20]             )
	s.add(target[14] ==        v[0]^v[1]^v[2]^v[3]^v[4]^v[7]^v[11]^v[12]^v[13]^v[15]^v[20]^v[21]  )
	s.add(target[15] == key ^  v[0]^v[1]^v[2]^v[3]^v[4]^v[5]^v[8]^v[12]^v[13]^v[14]^v[16]^v[21]         )
	
	s.add(target[16] == key ^  v[1]^v[2]^v[3]^v[4]^v[5]^v[6]^v[9]^v[13]^v[14]^v[15]^v[17]         )
	
	s.add(target[17] ==        v[0]^v[2]^v[3]^v[4]^v[5]^v[6]^v[7]^v[10]^v[14]^v[15]^v[16]^v[18]         )
	s.add(target[18] ==        v[1]^v[3]^v[4]^v[5]^v[6]^v[7]^v[8]^v[11]^v[15]^v[16]^v[17]^v[19]    ) 
	s.add(target[19] ==        v[2]^v[4]^v[5]^v[6]^v[7]^v[8]^v[9]^v[12]^v[16]^v[17]^v[18]^v[20]          )
	s.add(target[20] ==        v[3]^v[5]^v[6]^v[7]^v[8]^v[9]^v[10]^v[13]^v[17]^v[18]^v[19]^v[21] )
	s.add(target[21] == key ^  v[0]^v[4]^v[6]^v[7]^v[8]^v[9]^v[10]^v[11]^v[14]^v[18]^v[19]^v[20]        )
	

#	for i in range(len(target)):
#		s.add(target[i] < 126)

	#s.add(v[len(target) - 1] == 125)
	
	print(s.check())
	
	print(s.model())
	m = s.model()

	for i in range(len(target)):
		print(m[v[i]], end = ", ")

	print("\n")
	flag = ""

	for i in range(len(target)):
		flag += chr(m[v[i]].as_long())
# 13, 38, 14, 86, 39, 94, 124, 90, 33, 63, 101, 25, 44, 7, 119, 95, 1, 69, 114, 6, 17, 71,
	print(flag)





def cal():
	flag2 = []
	flagEncrypt = [107, 99, 115, 99, 116, 116, 97, 105, 110, 105, 110, 103, 123,    68, 68, 68, 69, 70, 71, 72, 73,     125]
	#flagEncrypt = [0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 1,     3, 0x2d, 0x0c, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0x0a, 0x44, 0x24, 0x2c]
                #   0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 0x1, 0x3, 0x2d, 0xc,  0x6f, 0x35, 0x61, 0x7e, 0x34,  0xa, 0x44, 0x24, 0x2c
	#encrypt(flagEncrypt)
	#flagEncrypt[1] += 20
	#encrypt(flagEncrypt)

	#target = [4, 70, 7, 111, 35, 34, 115, 39, 27, 113, 66, 123, 38, 39, 42, 77, 6, 64, 29, 106, 14, 120]
	target = [56, 50, 88, 115, 71, 94, 75, 2, 85, 36, 55, 118, 89, 30, 45, 101, 41, 31, 14, 10, 6, 75]
	for ai in range(len(flagEncrypt)):
			flag2.append(1)

	for i in range(len(flagEncrypt)): #loop so phan tu
		print(i, ": ", end = "")
		for j in range(len(flagEncrypt)): # loop test
			
			for ai in range(0, len(flagEncrypt)):
				flag2[ai] = flagEncrypt[ai]
			

			flag2[j] += 123
			encrypt(flag2)
			if(flag2[i] != target[i]):
				print("v[", end = "")
				print(j, end = "] ")
		
		print("")

	encrypt(flagEncrypt)


decrypt()
#cal()

#decrypt()
#&♫V'^|Z!?e↓,w_☺Er♠◄G
#flagEncrypt = [0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 1, 3, 0x2d, 0x0c, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0x0a, 0x44, 0x24, 0x2c]
#flagEncrypt = [13, 38, 14, 86, 39, 94, 124, 90, 33, 63, 101, 25, 44, 7, 119, 95, 1, 69, 114, 6, 17, 71]
#               13, 38, 14, 86, 39, 94, 124, 90, 33, 63, 101, 25, 44, 7, 119, 95, 1, 69, 114, 6, 17, 71
#flagEncrypt =  [107, 99, 115, 99, 116, 116, 97, 105, 110, 105, 110, 103, 123,    68, 68, 68, 69, 70, 71, 72, 73,     125]
#encrypt(flagEncrypt)
#print(flagEncrypt)
#for i in range(len(flagEncrypt)):
#	print(chr(flagEncrypt[i]), end = "")
#print("\n")
#encrypt(flagEncrypt)
#for i in range(len(flagEncrypt)):
#	print(hex(flagEncrypt[i]), end = ", ")

'''


target =  [4,     70,   7,    111, 35,    34,   115, 39,   27,   113, 66, 123,   38,   39,   42,   77,   6,   64,   29,   106,   14,   120]
#          4,     70,   7,    111, 35,    34,   115, 27,   27,   113, 66, 123,   38,   39,   42,   77,   6,   64,   29,   106,   14,   120
v = [0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 1, 3, 0x2d, 0x0c, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0x0a, 0x44, 0x24, 0x2c]

print( key ^   v[1]^v[6]^v[7]^v[9]^v[11]^v[13]^v[14]^v[15]^v[20]                  ,end = ", ")
print(         v[0]^v[2]^v[7]^v[8]^v[10]^v[12]^v[14]^v[15]^v[16]^v[21]                   ,end = ", ")
print( key ^   v[0]^v[1]^v[3]^v[8]^v[9]^v[11]^v[13]^v[15]^v[16]^v[17]               ,end = ", ")
print(         v[0]^v[1]^v[2]^v[4]^v[9]^v[10]^v[12]^v[14]^v[16]^v[17]^v[18]         ,end = ", ")
print(         v[1]^v[2]^v[3]^v[5]^v[10]^v[11]^v[13]^v[15]^v[17]^v[18]^v[19]               ,end = ", ")
print(         v[2]^v[3]^v[4]^v[6]^v[11]^v[12]^v[14]^v[16]^v[18]^v[19]^v[20]         ,end = ", ")
print(         v[3]^v[4]^v[5]^v[7]^v[12]^v[13]^v[15]^v[17]^v[19]^v[20]^v[21]        ,end = ", ")
print( key ^   v[0]^v[4]^v[5]^v[6]^v[8]^v[13]^v[14]^v[16]^v[18]^v[20]^v[21]         ,end = ", ")
print( key ^   v[1]^v[5]^v[6]^v[7]^v[9]^v[14]^v[15]^v[17]^v[19]^v[21]              ,end = ", ")
print( key ^   v[2]^v[6]^v[7]^v[8]^v[10]^v[15]^v[16]^v[18]^v[20]                   ,end = ", ")
print(         v[0]^v[3]^v[7]^v[8]^v[9]^v[11]^v[16]^v[17]^v[19]^v[21]                    ,end = ", ")
print(  key ^  v[0]^v[1]^v[4]^v[8]^v[9]^v[10]^v[12]^v[17]^v[18]^v[20]                   ,end = ", ")
print(         v[0]^v[1]^v[2]^v[5]^v[9]^v[10]^v[11]^v[13]^v[18]^v[19]^v[21]      ,end = ", ")
print(  key ^  v[0]^v[1]^v[2]^v[3]^v[6]^v[10]^v[11]^v[12]^v[14]^v[19]^v[20]             ,end = ", ")
print(         v[0]^v[1]^v[2]^v[3]^v[4]^v[7]^v[11]^v[12]^v[13]^v[15]^v[20]^v[21]  ,end = ", ")
print(  key ^  v[0]^v[1]^v[2]^v[3]^v[4]^v[5]^v[8]^v[12]^v[13]^v[14]^v[16]^v[21]         ,end = ", ")
print(  key ^  v[1]^v[2]^v[3]^v[4]^v[5]^v[6]^v[9]^v[13]^v[14]^v[15]^v[17]         ,end = ", ")
print(         v[0]^v[2]^v[3]^v[4]^v[5]^v[6]^v[7]^v[10]^v[14]^v[15]^v[16]^v[18]         ,end = ", ")
print(         v[1]^v[3]^v[4]^v[5]^v[6]^v[7]^v[8]^v[11]^v[15]^v[16]^v[17]^v[19]    ,end = ", ") 
print(         v[2]^v[4]^v[5]^v[6]^v[7]^v[8]^v[9]^v[12]^v[16]^v[17]^v[18]^v[20]          ,end = ", ")
print(         v[3]^v[5]^v[6]^v[7]^v[8]^v[9]^v[10]^v[13]^v[17]^v[18]^v[19]^v[21] ,end = ", ")
print(  key ^  v[0]^v[4]^v[6]^v[7]^v[8]^v[9]^v[10]^v[11]^v[14]^v[18]^v[19]^v[20]        ,end = ", ")

print("\n")
encrypt(v)
print(v)



'''




#  0        2                    7   8    9      11        13      15   16                 21
# [72, 50, 40, 115, 71, 94, 75, 114, 37, 84, 55, 6,   89, 110, 45, 21,  89, 31, 14, 10, 6, 59]
# [56, 50, 88, 115, 71, 94, 75, 2,   85, 36, 55, 118, 89, 30,  45, 101, 41, 31, 14, 10, 6, 75]

'''
a1 = [56, 50, 88, 115, 71, 94, 75, 2, 85, 36, 55, 118, 89, 30, 45, 101, 41, 31, 14, 10, 6, 75]
a2 = [104, 50, 8, 115, 71, 94, 75, 82, 5, 116, 55, 38, 89, 78, 45, 53, 121, 31, 14, 10, 6, 27]

for i in range(len(a1)):
	if(a1[i] != a2[i]):
		print(i, end = ", ")
'''