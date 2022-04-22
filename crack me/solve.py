flagEncrypt = [0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 1, 3, 0x2d, 0x0c, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0x0a, 0x44, 0x24, 0x2c]
flag2 = []

for i in range(len(flagEncrypt)):
	flag2.append(1)

#print(len(flagEncrypt))

for i in range(0, 0x539):
	#flag2[0] = flagEncrypt[0] ^ 0x50
	for j in range(0, len(flagEncrypt)):
		if(j == 0):
			flag2[j] = flagEncrypt[j] ^ 0x50
		else:
			flag2[j] = flagEncrypt[j] ^ flagEncrypt[j - 1]

	for ai in range(0, len(flagEncrypt)):
		flagEncrypt[ai] = flag2[ai]

print(flagEncrypt)