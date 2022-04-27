Có thể thấy hàm quan trọng nhất của chương trình là hàm kiểm tra flag thì đã bị thêm quá nhiều opcode rác

![t](https://user-images.githubusercontent.com/101321172/165465865-c22d65f2-1f35-40b2-921d-9a18978654f7.jpeg)

![t](https://user-images.githubusercontent.com/101321172/165466024-3a4f9ce7-aaa4-476b-9568-fed86653859b.jpeg)

Tuy nhiên chúng ta không biết chỗ nào mới là opcode rác để mà ```nop``` xong makecode, nên chúng ta sẽ debug chương trình để thấy luồng xử lý.

Em sẽ Debug bằng GDB, bới GDB tự động convert lệnh chứ không phải create instruction như IDA :D

Đặt breakpoint ở địa chỉ 004006DB (Địa chỉ call hàm ```check()```)

Ngoài ra chương trình cũng yêu cầu nhập flag trực tiếp làm đối số

![t](https://user-images.githubusercontent.com/101321172/165466753-87e6f51b-7504-4d4c-9849-e66505c512e1.jpeg)


![t](https://user-images.githubusercontent.com/101321172/165466895-820ee49c-eb07-4556-89ec-2430a03e1199.jpeg)


Có thể thấy trong hàm này có ```call``` đến 1 hàm khác, thử step vào đó

Ok giờ chúng ta thấy được vòng lặp đầu tiên

![t](https://user-images.githubusercontent.com/101321172/165467299-5f48ceae-a38e-4c18-a510-2748dd8ea478.jpeg)

Có thể hiểu là: 

```python
for i in range(0, 0x539)
```

Vòng lăp thứ 2:

![t](https://user-images.githubusercontent.com/101321172/165467852-cbf164d0-98c1-496e-8094-3b59e40096e5.jpeg)

```ecx``` giữ độ dài của chuỗi chúng ta nhập vào, nên có thể hiểu là 2 vòng lặp lồng nhau:

```python
for i in range(0, 0x539):
  for j in range(0, len(input)):
```

Hàm mã hóa bắt đầu tại địa chỉ 0x4007fc

![t](https://user-images.githubusercontent.com/101321172/165468282-f83e129c-af29-47d1-b88d-cb8b6b887762.jpeg)

Từng kí tự của input chúng ta nhập vào được đem xor với thanh ```r9b```, với giá trị trong ```r9b``` chính là ```key``` và được ```push 50h``` rồi ```pop r9``` ở bên trên

![t](https://user-images.githubusercontent.com/101321172/165469506-3a0ff222-9f43-4ce2-b5ba-6ab0de6c2bef.jpeg)

Đặt breakpoint tại địa chỉ này sau đó tiếp tục chạy chương trình, chúng ta thấy được giá trị trong r9b đã trở thành 0x74, ứng với kí tự ```t``` - ký tự đầu tiên trong input của chúng ta.

Hết mỗi round của ```j``` thì ```key``` sẽ được đổi thành giá trị cuối cùng của chuỗi input

Và đó chúng chính là thuật toán mã hóa mà chương trình sử dụng

```python

key = 0x50

def encrypt(flagEncrypt):

	flag2 = []

	for i in range(0, len(flagEncrypt)):
		flag2[i].append(flagEncrypt[i])
    
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

```

Đây là input của chúng ta sau khi ra khỏi hàm mã hóa 

![image](https://user-images.githubusercontent.com/101321172/165470217-1a91ee4e-cba1-47f5-a84c-359b71f72582.png)

Và cuối cùng sẽ được đem so sánh với 33 ký tự này

![t](https://user-images.githubusercontent.com/101321172/165470737-4bbbdfd8-1dad-4c8f-8b91-2fbd8cfddfc2.jpeg)

=> 33 ký tự đó chính là flag được mã hóa qua hàm mã hóa trên

Giờ nhiệm vụ của chúng ta là tìm ra giá trị ban đầu tự flag bị mã hóa

Để đi ngược lại thì có thể dùng z3 ngay từ đầu, nhưng em muốn thử nghiên cứu sâu hơn trong hàm mã hóa 1 chút :D

Quy luật của hàm mã hóa sẽ là:

![t](https://user-images.githubusercontent.com/101321172/165471751-6bee1143-6582-4cb3-91b7-db63faf38df5.jpeg)

Chúng ta thử quy hết về dòng đầu tiên

a3 = a2 ^ k1 = a1 ^ 0x50 ^ k1

b3 = a2 ^ b2 = a1 ^ 0x50 ^ a1 ^ b1 = b1 ^ 0x50

c3 = b2 ^ c2 = a1 ^ b1 ^ b1 ^ c1 = a1 ^ c1

d3 = d2 ^ k2 = c1 ^ d1 ^ d1 ^ k1 = c1 ^ k1

k3 = d2 ^ k2 = c1 ^ d1 ^ d1 ^ k1 = c1 ^ k1

=> Mỗi ký tự chỉ bị ảnh hưởng bới số các kí tự nhất định chứ không phải toàn bộ chuỗi ký tự, vì lệnh ```xor``` 2 lần với 1 giá trị sẽ trở lại giá trị ban đầu 

Lợi dụng điều này chúng ta có thể viết hàm bruteforce các ký tự bị ảnh hưởng

```python
def cal():
	flag2 = []
	
	#target = [ 0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 0x1, 0x3, 0x2d, 0xc, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0xa, 0x44, 0x24, 0x2c]
	target =  [0, 111, 31, 100, 8, 74, 8, 34, 106, 87, 22, 112, 102, 113, 73, 60, 115, 7, 81, 82, 75, 52, 111, 102, 109, 109, 47, 93, 99, 95, 8, 90, 85]


	#flagEncrypt = [13, 38, 14, 86, 39, 94, 124, 90, 33, 63, 101, 25, 44, 7, 119, 95, 1, 69, 114, 6, 17, 71]
	flagEncrypt =  [0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 1, 3, 0x2d, 0x0c, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0x0a, 0x44, 0x24, 0x2c, 0x4a, 0x46, 0x19, 0x59, 0x5b, 0x0e, 0x78, 0x74, 0x29, 0x13, 0x2c]

	for ai in range(len(flagEncrypt)):
			flag2.append(1)

	for i in range(len(flagEncrypt)): #loop so phan tu
		print(i, ": ", end = "")
		for j in range(len(flagEncrypt)): # loop test
			
			for ai in range(0, len(flagEncrypt)):
				flag2[ai] = flagEncrypt[ai]
			

			flag2[j] += 434
			encrypt(flag2)
			if(flag2[i] != target[i]):
				print("v[", end = "")
				print(j, end = "] ")
		
		print("")

	encrypt(flagEncrypt)

```


![t](https://user-images.githubusercontent.com/101321172/165472857-34b8ac15-2cf3-44b9-8ea7-4a8393fa46ac.jpeg)

Giờ còn các ký tự bị ảnh hưởng bởi ```key``` cũng tương tự


```python
target = [0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 1, 3, 0x2d, 0x0c, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0x0a, 0x44, 0x24, 0x2c, 0x4a, 0x46, 0x19, 0x59, 0x5b, 0x0e, 0x78, 0x74, 0x29, 0x13, 0x2c]
target2 = [0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 1, 3, 0x2d, 0x0c, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0x0a, 0x44, 0x24, 0x2c, 0x4a, 0x46, 0x19, 0x59, 0x5b, 0x0e, 0x78, 0x74, 0x29, 0x13, 0x2c]
encrypt(target)
key = 0x123
encrypt(target2)

for i in range(len(target2)):
	if(target2[i] != target[i]):
		print(i)
```

![t](https://user-images.githubusercontent.com/101321172/165473142-d261246e-6f76-423a-92aa-32e84f30370c.jpeg)


Ok giờ đã có đủ, giờ mới dùng z3 ==

```python
def sol():

	s = Solver()

	target = [0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 1, 3, 0x2d, 0x0c, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0x0a, 0x44, 0x24, 0x2c, 0x4a, 0x46, 0x19, 0x59, 0x5b, 0x0e, 0x78, 0x74, 0x29, 0x13, 0x2c]
	
	v = [BitVec("v%i"%i, 8) for i in range(len(target))]

	s.add(target[0] ^ key == v[0]^v[1]^v[5]^v[7]^v[11]^v[12]^v[13]^v[14]^v[18]^v[31]^v[32])
	s.add(target[1] ^ key == v[1]^v[2]^v[6]^v[8]^v[12]^v[13]^v[14]^v[15]^v[19]^v[32])
	s.add(target[2] ^ key == v[2]^v[3]^v[7]^v[9]^v[13]^v[14]^v[15]^v[16]^v[20])
	s.add(target[3] == v[0]^v[3]^v[4]^v[8]^v[10]^v[14]^v[15]^v[16]^v[17]^v[21])
	s.add(target[4] == v[1]^v[4]^v[5]^v[9]^v[11]^v[15]^v[16]^v[17]^v[18]^v[22])
	s.add(target[5] == v[2]^v[5]^v[6]^v[10]^v[12]^v[16]^v[17]^v[18]^v[19]^v[23])
	s.add(target[6] == v[3]^v[6]^v[7]^v[11]^v[13]^v[17]^v[18]^v[19]^v[20]^v[24])
	s.add(target[7] == v[4]^v[7]^v[8]^v[12]^v[14]^v[18]^v[19]^v[20]^v[21]^v[25])
	s.add(target[8] == v[5]^v[8]^v[9]^v[13]^v[15]^v[19]^v[20]^v[21]^v[22]^v[26])
	s.add(target[9] == v[6]^v[9]^v[10]^v[14]^v[16]^v[20]^v[21]^v[22]^v[23]^v[27])
	s.add(target[10] == v[7]^v[10]^v[11]^v[15]^v[17]^v[21]^v[22]^v[23]^v[24]^v[28])
	s.add(target[11] == v[8]^v[11]^v[12]^v[16]^v[18]^v[22]^v[23]^v[24]^v[25]^v[29])
	s.add(target[12] == v[9]^v[12]^v[13]^v[17]^v[19]^v[23]^v[24]^v[25]^v[26]^v[30])
	s.add(target[13] == v[10]^v[13]^v[14]^v[18]^v[20]^v[24]^v[25]^v[26]^v[27]^v[31])
	s.add(target[14] == v[11]^v[14]^v[15]^v[19]^v[21]^v[25]^v[26]^v[27]^v[28]^v[32])
	s.add(target[15] ^ key == v[0]^v[12]^v[15]^v[16]^v[20]^v[22]^v[26]^v[27]^v[28]^v[29])
	s.add(target[16] == v[0]^v[1]^v[13]^v[16]^v[17]^v[21]^v[23]^v[27]^v[28]^v[29]^v[30])
	s.add(target[17] == v[1]^v[2]^v[14]^v[17]^v[18]^v[22]^v[24]^v[28]^v[29]^v[30]^v[31])
	s.add(target[18] == v[2]^v[3]^v[15]^v[18]^v[19]^v[23]^v[25]^v[29]^v[30]^v[31]^v[32])
	s.add(target[19] ^ key == v[0]^v[3]^v[4]^v[16]^v[19]^v[20]^v[24]^v[26]^v[30]^v[31]^v[32])
	s.add(target[20] ^ key == v[1]^v[4]^v[5]^v[17]^v[20]^v[21]^v[25]^v[27]^v[31]^v[32])
	s.add(target[21] ^ key == v[2]^v[5]^v[6]^v[18]^v[21]^v[22]^v[26]^v[28]^v[32])
	s.add(target[22] ^ key == v[3]^v[6]^v[7]^v[19]^v[22]^v[23]^v[27]^v[29])
	s.add(target[23] == v[0]^v[4]^v[7]^v[8]^v[20]^v[23]^v[24]^v[28]^v[30])
	s.add(target[24] == v[1]^v[5]^v[8]^v[9]^v[21]^v[24]^v[25]^v[29]^v[31])
	s.add(target[25] == v[2]^v[6]^v[9]^v[10]^v[22]^v[25]^v[26]^v[30]^v[32])
	s.add(target[26] ^ key == v[0]^v[3]^v[7]^v[10]^v[11]^v[23]^v[26]^v[27]^v[31])
	s.add(target[27] == v[0]^v[1]^v[4]^v[8]^v[11]^v[12]^v[24]^v[27]^v[28]^v[32])
	s.add(target[28] ^ key == v[0]^v[1]^v[2]^v[5]^v[9]^v[12]^v[13]^v[25]^v[28]^v[29])
	s.add(target[29] == v[0]^v[1]^v[2]^v[3]^v[6]^v[10]^v[13]^v[14]^v[26]^v[29]^v[30])
	s.add(target[30] == v[1]^v[2]^v[3]^v[4]^v[7]^v[11]^v[14]^v[15]^v[27]^v[30]^v[31])
	s.add(target[31] == v[2]^v[3]^v[4]^v[5]^v[8]^v[12]^v[15]^v[16]^v[28]^v[31]^v[32])
	s.add(target[32] ^ key == v[0]^v[3]^v[4]^v[5]^v[6]^v[9]^v[13]^v[16]^v[17]^v[29]^v[32])

	print(s.check())

	m = s.model()

	for i in range(len(target)):
		print(chr(m[v[i]].as_long()), end= "")

```

![t](https://user-images.githubusercontent.com/101321172/165473483-c2dad4ca-8b5a-4b3d-892c-210b05188897.jpeg)


Code đầy đủ:

```python
from z3 import *

key = 0x50

def encrypt(flagEncrypt):

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



def cal():
	flag2 = []
	
	#target = [ 0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 0x1, 0x3, 0x2d, 0xc, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0xa, 0x44, 0x24, 0x2c]
	target =  [0, 111, 31, 100, 8, 74, 8, 34, 106, 87, 22, 112, 102, 113, 73, 60, 115, 7, 81, 82, 75, 52, 111, 102, 109, 109, 47, 93, 99, 95, 8, 90, 85]


	#flagEncrypt = [13, 38, 14, 86, 39, 94, 124, 90, 33, 63, 101, 25, 44, 7, 119, 95, 1, 69, 114, 6, 17, 71]
	flagEncrypt =  [0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 1, 3, 0x2d, 0x0c, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0x0a, 0x44, 0x24, 0x2c, 0x4a, 0x46, 0x19, 0x59, 0x5b, 0x0e, 0x78, 0x74, 0x29, 0x13, 0x2c]

	for ai in range(len(flagEncrypt)):
			flag2.append(1)

	for i in range(len(flagEncrypt)): #loop so phan tu
		print(i, ": ", end = "")
		for j in range(len(flagEncrypt)): # loop test
			
			for ai in range(0, len(flagEncrypt)):
				flag2[ai] = flagEncrypt[ai]
			

			flag2[j] += 434
			encrypt(flag2)
			if(flag2[i] != target[i]):
				print("v[", end = "")
				print(j, end = "] ")
		
		print("")

	encrypt(flagEncrypt)

def sol():

	s = Solver()

	target = [0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 1, 3, 0x2d, 0x0c, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0x0a, 0x44, 0x24, 0x2c, 0x4a, 0x46, 0x19, 0x59, 0x5b, 0x0e, 0x78, 0x74, 0x29, 0x13, 0x2c]
	
	v = [BitVec("v%i"%i, 8) for i in range(len(target))]

	s.add(target[0] ^ key == v[0]^v[1]^v[5]^v[7]^v[11]^v[12]^v[13]^v[14]^v[18]^v[31]^v[32])
	s.add(target[1] ^ key == v[1]^v[2]^v[6]^v[8]^v[12]^v[13]^v[14]^v[15]^v[19]^v[32])
	s.add(target[2] ^ key == v[2]^v[3]^v[7]^v[9]^v[13]^v[14]^v[15]^v[16]^v[20])
	s.add(target[3] == v[0]^v[3]^v[4]^v[8]^v[10]^v[14]^v[15]^v[16]^v[17]^v[21])
	s.add(target[4] == v[1]^v[4]^v[5]^v[9]^v[11]^v[15]^v[16]^v[17]^v[18]^v[22])
	s.add(target[5] == v[2]^v[5]^v[6]^v[10]^v[12]^v[16]^v[17]^v[18]^v[19]^v[23])
	s.add(target[6] == v[3]^v[6]^v[7]^v[11]^v[13]^v[17]^v[18]^v[19]^v[20]^v[24])
	s.add(target[7] == v[4]^v[7]^v[8]^v[12]^v[14]^v[18]^v[19]^v[20]^v[21]^v[25])
	s.add(target[8] == v[5]^v[8]^v[9]^v[13]^v[15]^v[19]^v[20]^v[21]^v[22]^v[26])
	s.add(target[9] == v[6]^v[9]^v[10]^v[14]^v[16]^v[20]^v[21]^v[22]^v[23]^v[27])
	s.add(target[10] == v[7]^v[10]^v[11]^v[15]^v[17]^v[21]^v[22]^v[23]^v[24]^v[28])
	s.add(target[11] == v[8]^v[11]^v[12]^v[16]^v[18]^v[22]^v[23]^v[24]^v[25]^v[29])
	s.add(target[12] == v[9]^v[12]^v[13]^v[17]^v[19]^v[23]^v[24]^v[25]^v[26]^v[30])
	s.add(target[13] == v[10]^v[13]^v[14]^v[18]^v[20]^v[24]^v[25]^v[26]^v[27]^v[31])
	s.add(target[14] == v[11]^v[14]^v[15]^v[19]^v[21]^v[25]^v[26]^v[27]^v[28]^v[32])
	s.add(target[15] ^ key == v[0]^v[12]^v[15]^v[16]^v[20]^v[22]^v[26]^v[27]^v[28]^v[29])
	s.add(target[16] == v[0]^v[1]^v[13]^v[16]^v[17]^v[21]^v[23]^v[27]^v[28]^v[29]^v[30])
	s.add(target[17] == v[1]^v[2]^v[14]^v[17]^v[18]^v[22]^v[24]^v[28]^v[29]^v[30]^v[31])
	s.add(target[18] == v[2]^v[3]^v[15]^v[18]^v[19]^v[23]^v[25]^v[29]^v[30]^v[31]^v[32])
	s.add(target[19] ^ key == v[0]^v[3]^v[4]^v[16]^v[19]^v[20]^v[24]^v[26]^v[30]^v[31]^v[32])
	s.add(target[20] ^ key == v[1]^v[4]^v[5]^v[17]^v[20]^v[21]^v[25]^v[27]^v[31]^v[32])
	s.add(target[21] ^ key == v[2]^v[5]^v[6]^v[18]^v[21]^v[22]^v[26]^v[28]^v[32])
	s.add(target[22] ^ key == v[3]^v[6]^v[7]^v[19]^v[22]^v[23]^v[27]^v[29])
	s.add(target[23] == v[0]^v[4]^v[7]^v[8]^v[20]^v[23]^v[24]^v[28]^v[30])
	s.add(target[24] == v[1]^v[5]^v[8]^v[9]^v[21]^v[24]^v[25]^v[29]^v[31])
	s.add(target[25] == v[2]^v[6]^v[9]^v[10]^v[22]^v[25]^v[26]^v[30]^v[32])
	s.add(target[26] ^ key == v[0]^v[3]^v[7]^v[10]^v[11]^v[23]^v[26]^v[27]^v[31])
	s.add(target[27] == v[0]^v[1]^v[4]^v[8]^v[11]^v[12]^v[24]^v[27]^v[28]^v[32])
	s.add(target[28] ^ key == v[0]^v[1]^v[2]^v[5]^v[9]^v[12]^v[13]^v[25]^v[28]^v[29])
	s.add(target[29] == v[0]^v[1]^v[2]^v[3]^v[6]^v[10]^v[13]^v[14]^v[26]^v[29]^v[30])
	s.add(target[30] == v[1]^v[2]^v[3]^v[4]^v[7]^v[11]^v[14]^v[15]^v[27]^v[30]^v[31])
	s.add(target[31] == v[2]^v[3]^v[4]^v[5]^v[8]^v[12]^v[15]^v[16]^v[28]^v[31]^v[32])
	s.add(target[32] ^ key == v[0]^v[3]^v[4]^v[5]^v[6]^v[9]^v[13]^v[16]^v[17]^v[29]^v[32])

	print(s.check())

	m = s.model()

	for i in range(len(target)):
		print(chr(m[v[i]].as_long()), end= "")


#cal()
#target = [0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 1, 3, 0x2d, 0x0c, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0x0a, 0x44, 0x24, 0x2c, 0x4a, 0x46, 0x19, 0x59, 0x5b, 0x0e, 0x78, 0x74, 0x29, 0x13, 0x2c]

#encrypt(target)

#print(target)

#cal()


sol()

'''
target = [0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 1, 3, 0x2d, 0x0c, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0x0a, 0x44, 0x24, 0x2c, 0x4a, 0x46, 0x19, 0x59, 0x5b, 0x0e, 0x78, 0x74, 0x29, 0x13, 0x2c]
target2 = [0x48, 0x5f, 0x36, 0x35, 0x35, 0x25, 0x14, 0x2c, 0x1d, 1, 3, 0x2d, 0x0c, 0x6f, 0x35, 0x61, 0x7e, 0x34, 0x0a, 0x44, 0x24, 0x2c, 0x4a, 0x46, 0x19, 0x59, 0x5b, 0x0e, 0x78, 0x74, 0x29, 0x13, 0x2c]
encrypt(target)
key = 0x123
encrypt(target2)

for i in range(len(target2)):
	if(target2[i] != target[i]):
		print(i)
'''
```
