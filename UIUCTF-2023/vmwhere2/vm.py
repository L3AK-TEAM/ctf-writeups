import sys


def jmp_offset(byte1, byte2):
    combined_bytes = (byte1 << 8) | byte2
    if combined_bytes > 32767:
        combined_bytes -= 65536
    return combined_bytes


COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"

M32 = 0xFFFFFFFF
M64 = 0xFFFFFFFFFFFFFFFF


def run(data):
    mem = [0 for _ in range(0x1000)]
    l18 = 0
    ip = 0
    saved_ip = 0

    ENABLE = False

    while 1:
        saved_ip = ip + 1
        match data[ip]:
            case 0:
                return 0

            case 1:
                tmp = (mem[l18 - 2] + mem[l18 - 1]) & 0xFF
                print(f"ADD {mem[l18-2]} {mem[l18-1]} = {tmp}")
                mem[l18 - 2] = tmp
                l18 -= 1
                ip = saved_ip

            case 2:
                tmp = (mem[l18 - 2] - mem[l18 - 1]) & 0xFF
                print(f"SUB {mem[l18-2]} {mem[l18-1]} = {tmp}")
                mem[l18 - 2] = tmp
                l18 -= 1
                ip = saved_ip

            case 3:
                tmp = (mem[l18 - 2] & mem[l18 - 1]) & 0xFF
                print(f"AND {mem[l18-2]} {mem[l18-1]} = {tmp}")
                mem[l18 - 2] = tmp
                l18 -= 1
                ip = saved_ip

            case 4:
                tmp = (mem[l18 - 2] | mem[l18 - 1]) & 0xFF
                print(f"OR {mem[l18-2]} {mem[l18-1]} = {tmp}")
                mem[l18 - 2] = tmp
                l18 -= 1
                ip = saved_ip

            case 5:
                if ENABLE:
                    print(l18, mem[:l18])
                tmp = (mem[l18 - 2] ^ mem[l18 - 1]) & 0xFF
                print(f"XOR {mem[l18-2]} {mem[l18-1]} = {tmp}")
                mem[l18 - 2] = tmp
                l18 -= 1
                ip = saved_ip

            case 6:
                tmp(mem[l18 - 2] << mem[l18 - 1] & 0x1F) & 0xFF
                print(f"LSHFT {mem[l18-2]} << {mem[l18-1] & 0x1f} = {tmp}")
                mem[l18 - 2] = tmp
                l18 -= 1
                ip = saved_ip

            case 7:
                tmp = (mem[l18 - 2] >> (mem[l18 - 1] & 0x1F)) & 0xFF
                print(f"RSHFT {mem[l18-2]} >> {(mem[l18-1] & 0x1f)} = {tmp}")
                mem[l18 - 2] = tmp
                l18 -= 1
                ip = saved_ip

            case 8:
                tmp = sys.stdin.read(1).encode()
                value = int.from_bytes(tmp, byteorder="big", signed=False)
                h = "{:02x}".format(value)
                print(f"READ {value} = {tmp} ({h})")
                mem[l18] = value
                l18 += 1
                ip = saved_ip

                print(f"({l18} : {mem[:l18]}")

            case 9:
                l18 -= 1
                print(f"WRITE {(mem[l18])}")
                sys.stdout.write(f"{COLOR_GREEN}{chr(mem[l18])}{COLOR_RESET}")
                sys.stdout.flush()
                ip = saved_ip

            case 10:
                h = "{:02x}".format(data[saved_ip])
                print(f"PUSH {data[saved_ip]} ({h})")
                mem[l18] = data[saved_ip]
                l18 += 1
                ip += 2

            case 0xB:
                print(f"TEST {mem[l18-1]}")
                off = jmp_offset(data[ip + 1], data[ip + 2])
                print(f"JNS {saved_ip + off}")
                ip = saved_ip
                ip += 2

            case 0xC:  # JZ
                print(f"TEST {mem[l18-1]}")
                off = jmp_offset(data[ip + 1], data[ip + 2])
                print(f"JZ {saved_ip + off}")
                if mem[l18 - 1] == 0:
                    saved_ip = saved_ip + off
                ip = saved_ip
                ip += 2

            case 0xD:  # JMP
                off = jmp_offset(data[ip + 1], data[ip + 2])

                print(f"JMP {saved_ip + off}")
                saved_ip = saved_ip + off

                ip = saved_ip
                ip += 2

            case 0xE:  # NOP
                print("POP")
                l18 -= 1
                ip = saved_ip

            case 0xF:
                print(f"DUP {mem[l18-1]}")
                mem[l18] = mem[l18 - 1]
                l18 += 1
                ip = saved_ip

            case 0x10:
                ip += 2
                tmp2 = data[saved_ip]
                print(f"REVERSE TOP {tmp2}")

                for i in range(tmp2 >> 1):
                    mem[l18 + (i - tmp2)], mem[l18 + ~i] = (
                        mem[l18 + ~i],
                        mem[l18 + (i - tmp2)],
                    )

            case 0x11:
                print("SPLIT BYTE TO BITS")
                l30 = mem[l18 - 1]
                for i in range(8):
                    mem[l18 - 1 + i] = l30 & 1
                    l30 >>= 1

                l18 += 7

                print(f"({l18} : {mem[:20]}")
                ip = saved_ip

            case 0x12:
                print("POP 8 VALUES, NEW VALUE = LSB OF LAST 8")
                l2f = 0
                for i in [7, 6, 5, 4, 3, 2, 1, 0]:
                    l2f = l2f << 1 | mem[l18 - 8 + i] & 1

                l18[-8] = l2f
                l18 -= 7
                ip = saved_ip

            case _:
                print(f"unknown opcode {data[ip]}")
                return


def dis(data):
    mem = [0 for _ in range(0x1000)]
    l18 = 0
    ip = 0
    saved_ip = 0

    while ip < len(data):
        saved_ip = ip + 1
        num = "{:>4}".format(ip)
        sys.stdout.write(f"[{num}] ")
        match data[ip]:
            case 0:
                print("EXIT")
                ip = saved_ip

            case 1:
                print("ADD")
                ip = saved_ip

            case 2:
                print("SUB")
                ip = saved_ip

            case 3:
                print("AND")
                ip = saved_ip

            case 4:
                print("OR")
                ip = saved_ip

            case 5:
                print("XOR")
                ip = saved_ip

            case 6:
                print("LSHIFT")
                ip = saved_ip

            case 7:
                print("RSHIFT")
                ip = saved_ip

            case 8:
                print("READ")
                ip = saved_ip

            case 9:
                print("WRITE")
                ip = saved_ip

            case 10:
                h = "{:02x}".format(data[saved_ip])
                print(f"PUSH {data[saved_ip]} ({h}) {repr(chr(data[saved_ip]))}")
                ip += 2

            case 0xB:
                off = jmp_offset(data[ip + 1], data[ip + 2])
                print(f"JNS {saved_ip + off}")
                ip = saved_ip
                ip += 2

            case 0xC:  # JZ
                off = jmp_offset(data[ip + 1], data[ip + 2])
                print(f"JZ {saved_ip + off + 2}")

                ip = saved_ip
                ip += 2

            case 0xD:  # JMP
                off = jmp_offset(data[ip + 1], data[ip + 2])
                print(f"JMP {saved_ip + off + 2}")

                ip = saved_ip
                ip += 2

            case 0xE:  # NOP
                print("POP")
                ip = saved_ip

            case 0xF:
                print("DUP")
                ip = saved_ip

            case 0x10:
                ip += 2
                tmp2 = data[saved_ip]
                print(f"REVERSE TOP {tmp2}")

            case 0x11:
                print("SPLIT BYTE TO BITS")

                # l18 += 7
                ip = saved_ip

            case 0x12:
                print("POP 8 VALUES, NEW VALUE = LSB OF LAST 8")
                ip = saved_ip

            case _:
                print(f"unknown opcode {data[ip]}")
                return


import sys
with open(sys.argv[1], "rb") as f:
    data = f.read()

dis(data)