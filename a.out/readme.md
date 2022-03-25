Có thể thấy bài này thì đọc code Disassembly còn đỡ lú hơn code Decompile C

Code disassembly:

![sned](https://user-images.githubusercontent.com/101321172/160092563-a7e617bb-df65-486c-9c1e-729430c75a28.jpg)

Code Decompile C:

![sned](https://user-images.githubusercontent.com/101321172/160092654-3b9a6f59-726e-45de-a793-b3b2c5ba4567.jpg)

Từ đoạn này: 

![sned](https://user-images.githubusercontent.com/101321172/160092764-6c5a2e03-2b7b-4c38-ad1a-a6266ebfe3df.jpg)

Có thể thấy xmm0 giữ input của chúng ta, sau đó đi qua 3 lệnh là ```pshufb```, ```paddd```, ```pxor```, sau đó được so sánh với giá trị ban đầu.

Nhiều người đọc đến đây thì sẽ nghĩ đến ngay angr bởi bài chỉ có một hàm ```strcmp()``` chứ không có các hàm mã hóa lằng nhằng.

Nhưng Puck angr, anh em tôi dùng z3 >:)

Đây đều là các thuật toán trên [sse](https://stackoverflow.com/questions/44299401/difference-between-mmx-and-xmm-register)

lệnh paddd: [tài liệu](https://www.felixcloutier.com/x86/paddb:paddw:paddd:paddq)

![sned](https://user-images.githubusercontent.com/101321172/160093907-8fb62315-ffb7-42f2-9ef8-e276a74130ad.jpg)

Là cộng 32 bit, thanh đầu tiên sẽ là thanh được cộng, thanh thứ 2 là thanh cộng, và kết quả trả về sẽ được lưu trong thanh đầu tiên

Vào mảng ```ADD32``` thu được mảng cộng

(Có vẻ tác giả cũng đã gợi ý cho chúng ta vì chia mảng này ra thành các từ có thể đọc được (13371337, Feeldeed, deadbeef bla bla))

![sned](https://user-images.githubusercontent.com/101321172/160094174-3fa724aa-51a2-48e6-86be-eb9fe14b8460.jpg)

Vì là cộng 32 bit, nên có thể chia thế này:

```python
add32 = [0x67637466, 0x13371337, 0xFEE1DEAD, 0xDEADBEEF]
```


pXor tương tự

![sned](https://user-images.githubusercontent.com/101321172/160096767-36318c57-dd00-4a30-bdb4-d6c85da5872d.jpg)

```python
xor = [0xAAF986EB, 0x34F823D4, 0x385F1A8D, 0x49B45876]
```

Bủh nhất thì vẫn là ```pshufb``` [link](https://www.felixcloutier.com/x86/pshufb)

![sned](https://user-images.githubusercontent.com/101321172/160096982-98e83f95-c5cc-4fd6-a0dc-12bf8d8c5f6f.jpg)
(Hiểu hộ)

Nhưng may mắn là có ông nào đó đã làm [video](https://www.youtube.com/watch?v=MOb9SZOdcXk) về phần này :V

![sned](https://user-images.githubusercontent.com/101321172/160097384-53fd65d7-d09b-4724-91c7-262d07f87bcf.jpg)

Mảng SHUFFLE tác giả cố tình gây lú vì để lẻ chỉ có 15 số các giá trị hex 8 bit, nhưng đó là lỗi của IDA, vì IDA coi 0x0001 = 0x1, nên nó bỏ luôn 2 số 0 ở đầu

Cái này đúng, nhưng trong trường hợp này thì sai, vì chúng ta cần mảng Shuffle có số phần tử là bội của 4 :v

Nên phải thêm ```0``` vào đầu

=> mảng shuffle: 

```python
SHUFFLE = [0, 0x0D, 0x0C, 0x0A, 0x08, 0x04, 0x0F, 0x03, 0x0E, 0x09, 0x0B, 0x05, 0x01, 0x07, 0x06, 0x02] # Packed Shuffle Bytes, may có cái video này :v   https://www.youtube.com/watch?v=MOb9SZOdcXk
```

Mảng này đóng vài trò làm index

VD:

pshufb xmm0, xmm1

Ví dụ trong xmm0 và xmm1 đang lưu trữ các giá trị:

xmm0 : 12, 56, 21, 25, 57

xmm1 : 3 , 0,  2,  1,  4

xmm0 sẽ là thanh ghi bị shuffle, xmm1 sẽ đóng vai trò làm index trong xmm0 mới

=> trả về xmm0 : 56, 57, 21, 25, 12

nói đơn giản là mảng SHUFFLE bên trên chính là index mới của flag mã hóa

flag khi qua lệnh pshufb thì các byte 8 bit sẽ được chuyển thứ tự theo ```SHUFFLE```, sau đó cứ 32 bit một được cộng với mảng ```add32```, rồi xor 32 bit với mảng ```xor```

flag mã hóa có được sẽ được đem so sánh với chính flag ban đầu, nếu 2 cái bằng nhau thì thành công

=> Chúng ta phải nối 4 ký tự một để thỏa mãn yêu cầu 32 bit (mỗi ký tự là 4 bit trong khoảng 0->0xff)

z3 có BitVec hỗ trợ các toán tử bitwise, trong đó có khai báo số bit sẽ dùng

![sned](https://user-images.githubusercontent.com/101321172/160098938-3a9eb714-e66d-4f8c-b290-c05057b05207.jpg)

Nhưng tuy nhiên chúng ta sẽ không khai báo 8 bit để tìm flag, bởi flag được nối cặp 4, nên cần đến 32 bit lần

# VD về z3 gây bủh

```python
from z3 import *

test = BitVec("test", 8)

s = Solver()

s.add(test << 8 == 0x4300)

s.check()

print(s.model())
```

Cách dùng thế này là sai, (thay << 8 bằng << 1 thì lại đúng vì z3 rất bủh):

![sned](https://user-images.githubusercontent.com/101321172/160099402-78f45a90-0f98-4a37-a1ad-26f325c24853.jpg)

Chúng ta nối 32 bit flag bằng thuật toán ```or```, nên chúng ta sẽ khai báo flag có 32 bit

```python
flagencrypt = [BitVec("flagencrypt%i" % i, 8 * 4) for i in range(0, 16)] # sau nối 4 cái vào với nhau
```

Nhưng nếu dùng thế này thì z3 có thể hiểu nhầm và tìm các số có 32 bit thật

nên chúng ta thêm điều kiện:

```python
for i in range(16):
	s.add(flagencrypt[i] >= 0, flagencrypt[i] <= 125) #Ascii printable zone
```

Chúng ta có thể nối flag theo cách này

![sned](https://user-images.githubusercontent.com/101321172/160100376-0188d587-27b5-42c9-99db-7c9b5a85ef14.jpg)

Ok code giải :v

```python
from z3 import *

#BYTE 8
#WORD 16
#DWORD 32
#QWORD 64

# Thứ tự: shuffle, add, xor

#xor = [0xAA, 0xF9, 0x86, 0xEB, 0x34, 0xF8, 0x23, 0xD4, 0x38, 0x5F, 0x1A, 0x8D, 0x49, 0xB4, 0x58, 0x76] # PXOR (64-bit operand) https://www.felixcloutier.com/x86/pxor 

xor = [0xAAF986EB, 0x34F823D4, 0x385F1A8D, 0x49B45876]
#      0AAF986EB 34F823D4 385F1A8D 49B45876
add32 = [0x67637466, 0x13371337, 0xFEE1DEAD, 0xDEADBEEF] # paddd: cộng 32 bit, 0xf là tối đa và chỉ có 4 bit => pack 8 cái một https://www.felixcloutier.com/x86/paddb:paddw:paddd:paddq

SHUFFLE = [0, 0x0D, 0x0C, 0x0A, 0x08, 0x04, 0x0F, 0x03, 0x0E, 0x09, 0x0B, 0x05, 0x01, 0x07, 0x06, 0x02] # Packed Shuffle Bytes, may có cái video này :v   https://www.youtube.com/watch?v=MOb9SZOdcXk
# 00 0D 0C 0A 08 04 0F 03 0E 09 0B 05 01 07 06 02

xor.reverse()
add32.reverse()			#stack mà :v
SHUFFLE.reverse()



flagencrypt = [BitVec("flagencrypt%i" % i, 8 * 4) for i in range(0, 16)] # sau nối 4 cái vào với nhau



s = Solver()

for i in range(16):
	s.add(flagencrypt[i] >= 0, flagencrypt[i] <= 125) #Ascii printable zone



s.add( (((flagencrypt[SHUFFLE[0]]) | (flagencrypt[SHUFFLE[1]] << 8) | (flagencrypt[SHUFFLE[2]] << 16) | (flagencrypt[SHUFFLE[3]] << 24)) + add32[0]) ^ xor[0] ==
		 ((flagencrypt[0]) | (flagencrypt[1] << 8 ) | (flagencrypt[2] << 16) | (flagencrypt[3] << 24)) ) 

s.add( (((flagencrypt[SHUFFLE[4]]) | (flagencrypt[SHUFFLE[5]] << 8) | (flagencrypt[SHUFFLE[6]] << 16) | (flagencrypt[SHUFFLE[7]] << 24)) + add32[1]) ^ xor[1] ==
		 ((flagencrypt[4]) | (flagencrypt[5] << 8 ) | (flagencrypt[6] << 16) | (flagencrypt[7] << 24)) ) 

s.add( (((flagencrypt[SHUFFLE[8]]) | (flagencrypt[SHUFFLE[9]] << 8) | (flagencrypt[SHUFFLE[10]] << 16) | (flagencrypt[SHUFFLE[11]] << 24)) + add32[2]) ^ xor[2] ==
		 ((flagencrypt[8]) | (flagencrypt[9] << 8 ) | (flagencrypt[10] << 16) | (flagencrypt[11] << 24)) ) 

s.add( (((flagencrypt[SHUFFLE[12]]) | (flagencrypt[SHUFFLE[13]] << 8) | (flagencrypt[SHUFFLE[14]] << 16) | (flagencrypt[SHUFFLE[15]] << 24)) + add32[3]) ^ xor[3] ==
		 ((flagencrypt[12]) | (flagencrypt[13] << 8 ) | (flagencrypt[14] << 16) | (flagencrypt[15] << 24)) ) 



print(s.check())

m = s.model()

#print(m)

flag = ""

for i in range(16):
	print( (m[flagencrypt[i]]) )
	flag += chr(m[flagencrypt[i]].as_long())

print(flag)

```
![sned](https://user-images.githubusercontent.com/101321172/160100548-9244c5e6-df1e-450b-b01c-aa601234b13e.jpg)


flag: CTF{S1MDf0rM3!}
