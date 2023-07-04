# **vmwhere2**

## **Description**
The challenge provides two files, a `chal` binary, and a `program`. We can run the program by calling `./chal program`. The behavior of this binary is almost identical to `vmwhere1`, as such I will skim through this one and jump straight to the disassembly.

The difference of this `chal` file however is that it adds a few more opcodes. Here are the additional ones:
```c
    case 0x10:
        local_20 = local_20 + 2;
        bVar2 = *pbVar1;
        if ((long)local_18 - (long)pbVar5 < (long)(ulong)bVar2) {
        printf("Stack underflow in reverse at 0x%04lx\n",(long)local_20 - (long)param_1);
        }
        for (local_2c = 0; (int)local_2c < (int)(uint)(bVar2 >> 1); local_2c = local_2c + 1) {
        bVar3 = local_18[(int)(local_2c - bVar2)];
        local_18[(int)(local_2c - bVar2)] = local_18[(int)~local_2c];
        local_18[(int)~local_2c] = bVar3;
        }
        break;
    case 0x11:
        local_30 = local_18[-1];
        for (local_28 = 0; local_28 < 8; local_28 = local_28 + 1) {
        (local_18 + -1)[local_28] = local_30 & 1;
        local_30 = local_30 >> 1;
        }
        local_18 = local_18 + 7;
        local_20 = pbVar1;
        break;
    case 0x12:
        local_2f = 0;
        for (local_24 = 7; -1 < local_24; local_24 = local_24 + -1) {
        local_2f = local_2f << 1 | (local_18 + -8)[local_24] & 1;
        }
        local_18[-8] = local_2f;
        local_18 = local_18 + -7;
        local_20 = pbVar1;
        break;
```

`0x10` rotates the top `N` values of the stack. `0x11` stores the value at the top of the stack in bits, where each bit is pushed to the stack. `0x12` will take the `lsb` of the top values of the stack and combine them into 1 value, essentially undoing `0x11`.

The python disassembler and processer that I wrote is the [same](vm.py), I just added those few additional instructions. 

[Here](program.dis) is the full disassembly of program. Its alot longer than vmwhere1. The reading and writing is the same, but the processing is different. Here is how 1 character is processed.
```
[ 116] PUSH 0 (00) '\x00' (called only once)
[ 118] READ
[ 119] SPLIT BYTE TO BITS
[ 120] PUSH 255 (ff) 'ÿ'
[ 122] REVERSE TOP 9
[ 124] REVERSE TOP 8
[ 126] PUSH 0 (00) '\x00'
[ 128] REVERSE TOP 2
[ 130] DUP
[ 131] PUSH 255 (ff) 'ÿ'
[ 133] XOR
[ 134] JZ 141
[ 137] POP
[ 138] JMP 145
[ 141] POP
[ 142] JMP 167
[ 145] REVERSE TOP 2
[ 147] REVERSE TOP 2
[ 149] JZ 159
[ 152] POP
[ 153] PUSH 1 (01) '\x01'
[ 155] ADD
[ 156] JMP 160
[ 159] POP
[ 160] DUP
[ 161] DUP
[ 162] ADD
[ 163] ADD
[ 164] JMP 128
[ 167] POP
```

Now I analyzed this in my python processor, and printed the memory at different stages of this process. It does some computation with the bits of each input then stores the full result as some number. After all is done, there will be an array of numbers on the stack based on this encoding.

Finally, it then just checks these values on the stack. 
```
[2418] PUSH 198 (c6) 'Æ'
[2420] XOR
[2421] REVERSE TOP 46
[2423] REVERSE TOP 47
[2425] OR
[2426] REVERSE TOP 46
[2428] REVERSE TOP 45
```

The double reverse is a way to get the first character. The OR essentially is the way to check if any character failed. The program computes:
```py
result = xor(target, magic(input))
acc = acc | result 
```

It then finally checks to ensure that `acc` is 0, which means that none of the XOR fails. Note that if even 1 XOR results in a number with a 1 bit, then acc will always be > 0, so the JZ will fail.
```
[2970] JZ 2976
[2973] JMP 3004
```

I didn't think too much about the encoding, but rather just emulated it. I noticed that it was independent to each character, so i built a dictionary with the mappings, then reversed the xor. When I first ran my script however, there were a few collisions between characters having the same output after that bit encoding.

```
collision: X and 1
collision: Z and 3
collision: \ and 5
collision: ^ and 7
collision: g and @
collision: o and H
collision: w and P
uiuctf{b4sZ_Z_Xs_b4sZd_just_lXkZ_vm_rZvZrsXng}
```

But seeing the reconstructed flag, and the collisions, I could assume that the `Z` should be `3` and `X` should be `1`. 

## **Solution**
```py
def f(bits):
    bits.append(255)
    bits[-2] = bits[-2] ^ bits[-1]; bits.pop()
    
    return bits[-1]

char_map = {}

for c in range(48, 126):
    bits = [int(b) for b in format(c, '08b')]
    bits = [0] + list(reversed(bits))
    bits.append(255)
    bits = [bits[0]] + [bits[-1]] + bits[1:-1] # REV 9, REV 8
    bits.append(0) # PUSH 0
    while 1: # 128
        bits[-1], bits[-2] = bits[-2], bits[-1] # REV 2
        bits.append(bits[-1]) # DUP

        if (f(bits) == 0): # PUSH 255, XOR, JZ
            bits.pop()
            break
        # FALL THROUGH 145
        bits.pop() 
        bits[-1], bits[-2] = bits[-2], bits[-1] # REV 2
        bits[-1], bits[-2] = bits[-2], bits[-1] # REV 2
        tmp = bits.pop()
        if tmp != 0:
            bits.append(1) # PUSH 1
            bits[-2] = bits[-2] + bits[-1] & 0xFF; bits.pop() #ADD
        bits.append(bits[-1]) #DUP
        bits.append(bits[-1]) #DUP
        bits[-2] = bits[-2] + bits[-1] & 0xFF #ADD
        bits.pop() 
        bits[-2] = bits[-2] + bits[-1] & 0xFF #ADD
        bits.pop()
    
    
    bits.pop()
    if(chr(c) == 'Z'):
            continue
    if(chr(c) == 'X'):
        continue
    
    if bits[-1] in char_map:
        print(f"collision: {chr(c)} and {char_map[bits[-1]]}")
    char_map[bits[-1]] = (chr(c))
    
target = [
  '198', '139', '217', '207', '99',  '96',
  '216', '123', '216', '96',  '246', '211',
  '123', '246', '216', '193', '207', '208',
  '246', '114', '99',  '117', '190', '246',
  '127', '216', '99',  '231', '109', '246',
  '99',  '207', '246', '216', '246', '216',
  '99',  '231', '109', '180', '136', '114',
  '112', '117', '184', '117'
]

t = reversed([int(x) for x in target])
print("".join(char_map[i] for i in t))
```

---
## **Flag**: uiuctf{b4s3_3_1s_b4s3d_just_l1k3_vm_r3v3rs1ng}
---

