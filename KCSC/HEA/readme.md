Hàm main cũng chính là hàm mã hóa flag nhập vào

![278992701_344588504319663_7684014743038322795_n](https://user-images.githubusercontent.com/101321172/165922556-f48ae753-09e9-4793-baea-033d49566a43.jpg)


```C
 if ( v8 > 0 )
  {
    flagPTR_raw = flag;
    do
    {
      Flag = *(_QWORD *)flagPTR_raw;
      i = 0i64;
      Flag2 = *((_QWORD *)flagPTR_raw + 1);
      j = 32i64;
      do
      {
        i += 0x123457898765432i64;
        Flag += (i + Flag2) ^ (16 * Flag2 - 0x1EC32D622D0480D8i64) ^ ((Flag2 >> 5) + 0x488D27F32AE91451i64);
        Flag2 += (i + Flag) ^ (16 * Flag - 0x2CBDA60BFD707FD3i64) ^ ((Flag >> 5) + 0x424F0D99A012A826i64);
        --j;
      }
      while ( j );
      *(_QWORD *)flagPTR_raw = Flag;
      *((_QWORD *)flagPTR_raw + 1) = Flag2;
      flagPTR_raw += 16;
      --v8;                                     // v8 = 5 4 3 2 1
    }
    while ( v8 );
  }
```

Có thể hiểu đơn giản là chương trình nối lần lượt 8 ký tự của flag vào biến ```Flag```, sau đó nối 8 ký tự tiếp theo vào biến ```Flag2``` rồi thực hiện mã hóa chúng bằng các thuật toán cộng và xor

```C
     Flag += (i + Flag2) ^ (16 * Flag2 - 0x1EC32D622D0480D8i64) ^ ((Flag2 >> 5) + 0x488D27F32AE91451i64);
     Flag2 += (i + Flag) ^ (16 * Flag - 0x2CBDA60BFD707FD3i64) ^ ((Flag >> 5) + 0x424F0D99A012A826i64);
```

Cuối cùng flag của chúng ta sẽ được đem so sánh với mảng:

```C
do
  {
    if ( flag[v16] != encrypted_flag[v16] )
    {
      puts("Wrong!");
      exit(1);
    }
    ++v3;
    ++v16;
  }
  while ( v3 < 0x50 );
```


Mảng encrypted_flag có 80 phần tử vì thế có thể gây nhầm lẫn rằng flag có 80 ký tự

Nhưng tuy nhiên, từ đoạn code bên trên

![278992701_344588504319663_7684014743038322795_n](https://user-images.githubusercontent.com/101321172/165923135-721f8d31-7afd-4e0e-8a39-76a5dd91abfd.jpg)

Đoạn code này check và nối giá trị ```0xcc``` vào mảng flag nếu nó chưa đủ độ dài, ở đây là 80, do đó chúng ta có:

len(flag) + v4 - len(flag) == 80

=> v4 == 80

=> len(flag) + v7 == 80

=> len(flag) + (16 - len(flag) & 0xf) == 80

Ngoài ra còn điều kiện: len(flag) & 0xf != 0

Mà 80 & 0xf == 0 => flag không thể có 80 phần tử

Mà thực ra đoán số phần tử của flag cũng chẳng giải quyết được gì >:l

Mảng ```encrypted_flag``` là kết quả của ```flag``` sau khi qua hàm mã hóa và tách các ký tự ra, nên chúng ta chỉ cần đi ngược lại hàm này bằng cách nối các ký tự trong mảng ```encrypted_flag``` lại, sau đó đi ngược lại hàm mã hóa:


```C
      do
      {
        i += 0x123457898765432i64;
        Flag += (i + Flag2) ^ (16 * Flag2 - 0x1EC32D622D0480D8i64) ^ ((Flag2 >> 5) + 0x488D27F32AE91451i64);
        Flag2 += (i + Flag) ^ (16 * Flag - 0x2CBDA60BFD707FD3i64) ^ ((Flag >> 5) + 0x424F0D99A012A826i64);
        --j;
      }
      while ( j );
```


Để đi ngược lại hàm thì chúng ta cần tính ```i``` trước

May mắn là hàm mã hóa phần lớn là lệnh xor, nên chúng ta chỉ cần xor lại.

Code giải:

```C
#include <iostream>

int main(){
	unsigned __int64 flag  = 0x49d5350d575ca310;
	unsigned __int64 flag2 = 0xbffc208e9ef90f6a;

	unsigned __int64 flag3 = 0x644681c7bb0cb7a2;
	unsigned __int64 flag4 = 0x83e83897e0b61bea;

	unsigned __int64 flag5 = 0x13ce365e5a9f6ddd;
	unsigned __int64 flag6 = 0x5b575f2b16d0f43d;

	unsigned __int64 flag7 = 0xe537e3c7e41557c0;
	unsigned __int64 flag8 = 0x89bda52571c130de;

	unsigned __int64 flag9 = 0x2c9b3c6c4919e15f;
	unsigned __int64 flag10 = 0x30a09411d777e851;

	__int64 i = 0;

	__int64 j = 32, v8 = 5;

	do{

		i += 0x123457898765432;
		--j;
	}
	while(j);

	j = 32;
		do{
			flag2 -= (i + flag) ^ (16 * flag - 0x2CBDA60BFD707FD3) ^ ((flag >> 5) + 0x424F0D99A012A826);
			flag -= (i + flag2) ^ (16 * flag2 - 0x1EC32D622D0480D8) ^ ((flag2 >> 5) + 0x488D27F32AE91451);

			flag4 -= (i + flag3) ^ (16 * flag3 - 0x2CBDA60BFD707FD3) ^ ((flag3 >> 5) + 0x424F0D99A012A826);
			flag3 -= (i + flag4) ^ (16 * flag4 - 0x1EC32D622D0480D8) ^ ((flag4 >> 5) + 0x488D27F32AE91451);

			flag6 -= (i + flag5) ^ (16 * flag5 - 0x2CBDA60BFD707FD3) ^ ((flag5 >> 5) + 0x424F0D99A012A826);
			flag5 -= (i + flag6) ^ (16 * flag6 - 0x1EC32D622D0480D8) ^ ((flag6 >> 5) + 0x488D27F32AE91451);

			flag8 -= (i + flag7) ^ (16 * flag7 - 0x2CBDA60BFD707FD3) ^ ((flag7 >> 5) + 0x424F0D99A012A826);
			flag7 -= (i + flag8) ^ (16 * flag8 - 0x1EC32D622D0480D8) ^ ((flag8 >> 5) + 0x488D27F32AE91451);

			flag10 -= (i + flag9) ^ (16 * flag9 - 0x2CBDA60BFD707FD3) ^ ((flag9 >> 5) + 0x424F0D99A012A826);
			flag9 -= (i + flag10) ^ (16 * flag10 - 0x1EC32D622D0480D8) ^ ((flag10 >> 5) + 0x488D27F32AE91451);
			//std::cout << "0x" <<std::hex << flag << "\n";
			i -= 0x123457898765432;
			--j;
		}

		while(j);
		
	std::cout <<  "0x" <<std::hex << flag << "\n";
	std::cout  << "0x"<< std::hex << flag2 << "\n";
	std::cout  << "0x"<< std::hex << flag3 << "\n";
	std::cout  << "0x"<< std::hex << flag4 << "\n";
	std::cout  << "0x"<< std::hex << flag5 << "\n";
	std::cout  << "0x"<< std::hex << flag6 << "\n";
	std::cout  << "0x"<< std::hex << flag7 << "\n";
	std::cout  << "0x"<< std::hex << flag8 << "\n";
	std::cout  << "0x"<< std::hex << flag9 << "\n";
	std::cout  << "0x"<< std::hex << flag10 << "\n";
}
```

flag: KCSC{833N_5p3nD1N'_m057_7H31r_L1v35_l1v1n'_1n_7H3_G4ng574'5_p4R4d123}
