passwd = "P45sW0rd_cr4ck3r_G0_g0!!!"

new = ""

a = 0

for i in range (len(passwd)):
	a += 1
	new += chr((ord(passwd[i]) ^ ord(passwd[i+1])))

print(new)