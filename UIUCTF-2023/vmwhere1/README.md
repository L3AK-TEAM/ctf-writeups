# **vmwhere1**

## **Description**
The challenge provides two files, a `chal` binary, and a `program`. We can run the program by calling `./chal program`.

```console
abhi@abhi-omen:~/UIUCTF/wmwhere/vmwhere1$ ./chal program
Welcome to VMWhere 1!
Please enter the password:
asdf
Icorrect password!
```

`chal` is a processor of some kind and program contains the actual executable we will need to use to try and find the password. One interesting thing we can see already about the program is that the strings are spaced apart and reversed.

```
00000000: 0a00 0a0a 0a21 0a31 0a20 0a65 0a72 0a65  .....!.1. .e.r.e
00000010: 0a68 0a57 0a4d 0a56 0a20 0a6f 0a74 0a20  .h.W.M.V. .o.t.
00000020: 0a65 0a6d 0a6f 0a63 0a6c 0a65 0a57 0c00  .e.m.o.c.l.e.W..
00000030: 0409 0dff f90a 000a 0a0a 3a0a 640a 720a  ..........:.d.r.
00000040: 6f0a 770a 730a 730a 610a 700a 200a 650a  o.w.s.s.a.p. .e.
00000050: 680a 740a 200a 720a 650a 740a 6e0a 650a  h.t. .r.e.t.n.e.
00000060: 200a 650a 730a 610a 650a 6c0a 500c 0004   .e.s.a.e.l.P...
00000070: 090d fff9 0a00 080f 0a04 0705 050f 0a72  ...............r
00000080: 050c 0003 0d04 0d0e 080f 0a04 0705 050f  ................
00000090: 0a1d 050c 0003 0d03 fb0e 080f 0a04 0705  ................
000000a0: 050f 0a6f 050c 0003 0d03 e90e 080f 0a04  ...o............
000000b0: 0705 050f 0a0a 050c 0003 0d03 d70e 080f  ................
000000c0: 0a04 0705 050f 0a79 050c 0003 0d03 c50e  .......y........
000000d0: 080f 0a04 0705 050f 0a19 050c 0003 0d03  ................
...
```

My first plan in working towards this challenge is to write my own processor and disassembler. This would allow me to finer control the program execution. While this might have been a bit overkill, since there were two vmwhere challenges I assumed this would useful later on as well.

First, lets look at the binary in Ghidra to understand what the opcodes are and how they work. We can find the entry point from `libc_start_main` and start looking at the program flow from there.

```c
undefined8 FUN_001018e6(int param_1,undefined8 *param_2)
{
  undefined8 uVar1;
  long in_FS_OFFSET;
  undefined4 local_20;
  int local_1c;
  long local_18;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  if (param_1 < 2) {
    printf("Usage: %s <program>\n",*param_2);
    uVar1 = 1;
  }
  else {
    local_18 = FUN_001012a9(param_2[1],&local_20);
    if (local_18 == 0) {
      printf("Failed to read program %s\n",param_2[1]);
      uVar1 = 2;
    }
    else {
      local_1c = FUN_0010144c(local_18,local_20);
      if (local_1c == 0) {
        uVar1 = 0;
      }
      else {
        uVar1 = 3;
      }
    }
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return uVar1;
  ```

The main function is pretty clear to understand. It makes a call to `FUN_001012a9` which loads the program from the file, and stores the program length in `local_20`. We then run the program with `FUN_0010144c`. `FUN_0010144c` is where the actual runtime happens. The function is essentially just a while loop that keeps reading operations and does the associated actions.

For instance, here is the first few operations of the program:
```c
undefined8 FUN_0010144c(byte *param_1,int param_2)
{
  byte *pbVar1;
  byte bVar2;
  byte bVar3;
  int iVar4;
  byte *pbVar5;
  uint local_24;
  byte *local_20;
  byte *local_18;
  
  pbVar5 = (byte *)malloc(0x1000);
  local_20 = param_1;
  local_18 = pbVar5;
  while( true ) {
    if ((local_20 < param_1) || (param_1 + param_2 <= local_20)) {
      printf("Program terminated unexpectedly. Last instruction: 0x%04lx\n",
             (long)local_20 - (long)param_1);
      return 1;
    }
    pbVar1 = local_20 + 1;
    switch(*local_20) {
    case 0:
      return 0;
    case 1:
      local_18[-2] = local_18[-2] + local_18[-1];
      local_18 = local_18 + -1;
      local_20 = pbVar1;
      break;
    case 2:
      local_18[-2] = local_18[-2] - local_18[-1];
      local_18 = local_18 + -1;
      local_20 = pbVar1;
      break;
    case 3:
      local_18[-2] = local_18[-2] & local_18[-1];
      local_18 = local_18 + -1;
      local_20 = pbVar1;
      break;
```

`local_20` is the instruction pointer, and `local_18` is the stack pointer. The full instruction set is the following. `ADD`, `SUB`, `AND`, `OR`, `XOR`, `LSFT`, `RSFT`, `READ`, `WRITE`, `JNS`, `JZ`, `JMP`, `POP`, `DUP`. (vmwhere2 adds a few more which will be added in that writeup.)

I then rewrote this into my own runtime and disassembler using python. The full code for that can be found [here](vm.py). I then used this to disassemble the program.


[Here](program.dis) is the full disassembly of program. Below I will note how the disassembly looks like and how I was able to solve the challenge.

The program prints strings by first pushing the string in reverse, where the first charecter is the final null terminator.
```
[   0] PUSH 0 (00) '\x00'
[   2] PUSH 10 (0a) '\n'
[   4] PUSH 33 (21) '!'
[   6] PUSH 49 (31) '1'
[   8] PUSH 32 (20) ' '
[  10] PUSH 101 (65) 'e'
[  12] PUSH 114 (72) 'r'
[  14] PUSH 101 (65) 'e'
[  16] PUSH 104 (68) 'h'
[  18] PUSH 87 (57) 'W'
[  20] PUSH 77 (4d) 'M'
[  22] PUSH 86 (56) 'V'
[  24] PUSH 32 (20) ' '
[  26] PUSH 111 (6f) 'o'
[  28] PUSH 116 (74) 't'
[  30] PUSH 32 (20) ' '
[  32] PUSH 101 (65) 'e'
[  34] PUSH 109 (6d) 'm'
[  36] PUSH 111 (6f) 'o'
[  38] PUSH 99 (63) 'c'
[  40] PUSH 108 (6c) 'l'
[  42] PUSH 101 (65) 'e'
[  44] PUSH 87 (57) 'W'
```

It then uses this loop to pop and print these values.
```
[  46] JZ 53
[  49] WRITE
[  50] JMP 46
```

Which repeatedly calls write on the top of the stack consuming the character, until the final null terminator `0` is reached causing a jump out of here. 

Following this, we have 57 `READ` blocks, which reads each character of the input flag. They each look like this:

```
[ 116] PUSH 0 (00) '\x00' (only pushed once in the beginning)
[ 118] READ
[ 119] DUP
[ 120] PUSH 4 (04) '\x04'
[ 122] RSHIFT
[ 123] XOR
[ 124] XOR
[ 125] DUP
[ 126] PUSH 114 (72) 'r'
[ 128] XOR
[ 129] JZ 135
[ 132] JMP 1172
[ 135] POP
```

One advantage of writing a processor for this as well, as it lets me get extremely easy to understand operations since I can inspect runtime memory as well. Here is the result of the live disassembly.

```
PUSH 0 (00)
uiuctf{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}
READ 117 = b'u' (75)
(4 : [0, 0, 0, 117]
DUP 117
PUSH 4 (04)
RSHFT 117 >> 4 = 7
XOR 117 7 = 114
XOR 0 114 = 114
DUP 114
PUSH 114 (72)
XOR 114 114 = 0
TEST 0
JZ 133
POP
READ 105 = b'i' (69)
(4 : [0, 0, 114, 105]
DUP 105
PUSH 4 (04)
RSHFT 105 >> 4 = 6
XOR 105 6 = 111
XOR 114 111 = 29
DUP 29
PUSH 29 (1d)
XOR 29 29 = 0
TEST 0
JZ 151
POP
```

So now we exactly know whats going on. Let `c` be the input. We first compute,
```py
tmp = c ^ (c >> 4) 
```

We then xor this with the previous value on the stack, which would be `0` for this first case, but we can also see in the disassembly the second character is compared to the output of the first character. We then test this with a new target thats pushed from the stack.

```py
if target != tmp ^ results[-1]:
    jump(FAIL)
```

Using this, I simply grabbed the target values from the binary, and found the values that made it work to get the flag.


## **Solution**
```py
inputs = []
prev_thing = [0]
targets = [
  0x72, 0x1d, 0x6f, 0x0a, 0x79,
  0x19, 0x65, 0x02, 0x77, 0x47,
  0x1d, 0x63, 0x50, 0x22, 0x78,
  0x4f, 0x15, 0x60, 0x50, 0x37,
  0x5d, 0x07, 0x76, 0x1d, 0x47,
  0x37, 0x59, 0x69, 0x1c, 0x2c,
  0x76, 0x5c, 0x3d, 0x4a, 0x39,
  0x63, 0x02, 0x32, 0x5a, 0x6a,
  0x1f, 0x28, 0x5b, 0x6b, 0x09,
  0x53, 0x20, 0x4e, 0x7c, 0x08,
  0x52, 0x32, 0x00, 0x37, 0x56,
  0x7d, 0x07
]

for target in targets:
    for i in range(ord('!'), 127):
        tmp = ((i >> 4) & 0xFF)
        tmp = (tmp ^ i) & 0xFF
        tmp = (prev_thing[-1] ^ tmp) & 0xFF
        if tmp == target:
            prev_thing.append(target)
            inputs.append(chr(i))

print(''.join(inputs))
```

---
## **Flag**: uiuctf{ar3_y0u_4_r3al_vm_wh3r3_(gpt_g3n3r4t3d_th1s_f14g)}
---

