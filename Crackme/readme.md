Có thể thấy hàm quan trọng nhất của chương trình là hàm kiểm tra flag thì đã bị thêm quá nhiều opcode rác

![t](https://user-images.githubusercontent.com/101321172/165465865-c22d65f2-1f35-40b2-921d-9a18978654f7.jpeg)

![t](https://user-images.githubusercontent.com/101321172/165466024-3a4f9ce7-aaa4-476b-9568-fed86653859b.jpeg)

Tuy nhiên chúng ta không biết chỗ nào mới là opcode rác để mà ```nop``` xong makecode, nên chúng ta sẽ debug chương trình để thấy luồng xử lý.

Em sẽ Debug bằng GDB

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

Từng kí tự của input chúng ta nhập vào được đem xor với thanh ```r9b```, với giá trị trong ```r9b``` được ```push 50h``` rồi ```pop r9``` ở bên trên

![image](https://user-images.githubusercontent.com/101321172/165468556-6a8fc88e-e8f3-4afa-90f1-8b1b63fe6952.png)

Đặt breakpoint tại địa chỉ này sau đó tiếp tục chạy chương trình, chúng ta thấy được giá trị trong r9b đã trở thành 0x74, ứng với kí tự ```t``` - ký tự đầu tiên trong input của chúng ta.

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
