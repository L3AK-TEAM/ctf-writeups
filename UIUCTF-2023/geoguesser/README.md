# **geoguesser**
#### I thought geoguesser was too easy, so I made it harder.

## **Description**
We are given a binary called `janet` and a file `program.jimage`. We can run the program in the following way:
```console
abhi@abhi-omen:~/UIUCTF/janet$ ./janet -i program.jimage
Welcome to geoguesser!
Where am I? 5, 9
Nope. You have 4 guesses left.
Where am I? 45, 11
Nope. You have 3 guesses left.
Where am I? 34 -129
Not a valid coordinate. Try again.
Where am I? 33, 56
Nope. You have 2 guesses left.
Where am I? 1, 1
Nope. You have 1 guesses left.
Where am I? 0, 0
You lose!
The answer was: <tuple 0x5627A0DD4BC0>
```

We need to guess a coordinate within 5 guesses. But we are given no information at all whether our guess is correct or not. We are not even told the correct answer if we fail. 

Time to reverse! I searched up `janet`, and found the [github](https://github.com/janet-lang/janet) and [documentation](https://janet-lang.org/docs/index.html). Its actually a pretty well documented `Clojure` like functional language.

Immediately, the first thing that came to my mind was, maybe the `.jimage` file is kind of like a `.pyc` file? If so, just like in python, wouldn't that mean I can just import it? Turns out? YES!

```clojure
abhi@abhi-omen:~/UIUCTF/janet$ ./janet
Janet 1.28.0-358f5a0 linux/x64/gcc - '(doc)' for help
repl:1:> (import ./program)
@{_ @{:value <cycle 0>} program/compare-coord @{:private true} program/compare-float @{:private true} program/coordinate-peg @{:private true} program/get-guess @{:private true} program/guessing-game @{:private true} program/init-rng @{:private true} program/main @{:private true} program/parse-coord @{:private true} program/precision @{:private true} program/print-flag @{:private
 true} program/random-float @{:private true} program/rng @{:private true} :macro-lints @[]}
 ```

We can already see all the functions in Janet. A quick look at the documentation notes:
> If you create a "main" function, janet will automatically call that for you when you run your script.

And sure enough, calling `(program/main)` runs the program.
```clojure
repl:2:> (program/main)
Welcome to geoguesser!
Where am I? 4, 7
Nope. You have 4 guesses left.
```

I read a bit more of the documentation to understand how the program is actually compiled. I found the following [reference](https://janet-lang.org/api/index.html) for a function called `disasm` which is part of the `janet` core library. 

```
disasm
(disasm func &opt field)

Returns assembly that could be used to compile the given function. func must be a function, not a c function. Will throw on error on a badly typed argument. If given a field name, will only return that part of the function assembly. Possible fields are:

* :arity - number of required and optional arguments.
* :min-arity - minimum number of arguments function can be called with.
* :max-arity - maximum number of arguments function can be called with.
* :vararg - true if function can take a variable number of arguments.
* :bytecode - array of parsed bytecode instructions. Each instruction is a tuple.
* :source - name of source file that this function was compiled from.
* :name - name of function.
* :slotcount - how many virtual registers, or slots, this function uses. Corresponds to stack space used by function.
* :symbolmap - all symbols and their slots.
* :constants - an array of constants referenced by this function.
* :sourcemap - a mapping of each bytecode instruction to a line and column in the source file.
* :environments - an internal mapping of which enclosing functions are referenced for bindings.
* :defs - other function definitions that this function may instantiate.
```

I used it on `program/main` and got the full disassembly:
```clojure
repl:1:> (import ./program)
@{_ @{:value <cycle 0>} program/compare-coord @{:private true} program/compare-float @{:private true} program/coordinate-peg @{:private true} program/get-guess @{:private true} program/guessing-game @{:private true} program/init-rng @{:private true} program/main @{:private true} program/parse-coord @{:private true} program/precision @{:private true} program/print-flag @{:private
 true} program/random-float @{:private true} program/rng @{:private true} :macro-lints @[]}
repl:2:> (disasm program/main)
{:arity 0 :bytecode @[ (lds 0) (ldc 1 0) (push 1) (ldc 2 1) (call 1 2) (ldc 3 2) (call 2 3) (ldi 3 -90) (ldi 4 90) (push2 3 4) (ldc 4 3) (call 3 4) (ldi 4 -180) (ldi 5 180) (push2 4 5) (ldc 5 3) (call 4 5) (push2 3 4) (mktup 3) (movn 4 3) (push 4) (ldc 6 4) (call 5 6) (jmpno 5 3) (ldc 6 5) (tcall 6) (ldc 6 6) (push 6) (ldc 7 1) (call 6 7) (ldc 6 7) (push2 6 4) (ldc 6 1) (tcall 6)] :constants @["Welcome to geoguesser!" <cfunction print> <function init-rng> <function random-float> <function guessing-game> <function print-flag> "You lose!" "The answer was: "] :defs @[] :environments @[] :max-arity 2147483647 :min-arity 0 :name "main" :slotcount 8 :source "main.janet" :sourcemap @[ (54 1) (55 3) (55 3) (55 3) (55 3) (56 3) (56 3) (57 16) (57 16) (57 16) (57 16) (57 16) (57 38) (57 38) (57 38) (57 38) (57 38) (57 15) (57 15) (57 3) (58 7) (58 7) (58 7) (58 3) (59 5) (59 5) (61 7) (61 7) (61 7) (61 7) (62 7) (62 7) (62 7) (62 7)] :structarg false :symbolmap @[(0 34 0 main) (19 34 4 answer)] :vararg false}
```

So we seem to have a series of objects returned in the disassembly. The `bytecode` array and `constants` are probably the most interesting. The `bytecode` array seems to have common instructions such as load, call, push. I looking to find the opcodes, and found it [here](https://janet-lang.org/docs/abstract_machine.html) (once again very well documented).

In short, `janet` uses `virtual registers` or `slots` that the bytecode interprets, which are stored on the stack. Some of numbers in the bytecode disasembly are referring to those slots. For example:

```asm
ldc 1 0
push 1
ldc 2 1
call 1 2
```

Is equivalent to:
```py
_1 = constants[0] #"Welcome to geoguesser!"
_2 =  constance[1] # <cfunction print>
_2(_1)
```
Which just prints "Welcome to geoguesser!". The code itself is pretty short so we can skim through this. We can see that later in the bytecode,

```py
ldi 3 -90 
ldi 4 90
push2 3 4
ldc 4 3 # <function random-float>
call 3 4 # random-float(-90, 90)
```

Is setting up a function call to get a random-float between -90 and 90. This is probably the latitude we need to guess. It also later does the same thing for -180 to 180, so this is exactly the values we would need to figure out.

```clojure
repl:3:> (disasm program/random-float)
{:arity 2 :bytecode @[ (lds 2) (ldc 3 0) (geti 3 3 0) (push 3) (ldc 4 1) (call 3 4) (sub 4 1 0) (mul 5 3 4) (add 3 0 5) (ret 3)] :constants @[@[nil] <cfunction math/rng-uniform>] :defs @[] :environments @[] :max-arity 2 :min-arity 2 :name "random-float" :slotcount 6 :source "main.janet" :sourcemap @[ (51 1) (52 13) (52 13) (52 13) (52 13) (52 13) (52 36) (52 10) (52 3) (52 3)] :structarg false :symbolmap @[(0 10 0 min) (0 10 1 max) (0 10 2 random-float)] :vararg false}
```

The `random-float` function is quite short. It only makes one call to `math/rng-uniform` then scales the value with `sub`, `mul`, `add` to fit the wanted window. Now one thing that stumped me initially is that `rng-uniform` actually takes an argument `(core/rng)` which doesn't seem to be showed here, but I later realized that I had overlooked the `init-rng` function.

```clojure
repl:2:> (disasm program/init-rng)
{:arity 0 :bytecode @[ (lds 0) (ldc 2 0) (call 1 2) (push 1) (ldc 3 1) (call 2 3) (ldc 1 2) (puti 1 2 0) (ldc 1 2) (geti 1 1 0) (ret 1)] :constants @[<cfunction os/time> <cfunction math/rng> @[nil]] :defs @[] :environments @[] :max-arity 0 :min-arity 0 :name "init-rng" :slotcount 4 :source "main.janet" :sourcemap @[ (5 1) (6 22) (6 22) (6 12) (6 12) (6 12) (6 12) (6 12) (6 3) (6
 3) (6 3)] :structarg false :symbolmap @[(0 11 0 init-rng)] :vararg false}
```

Ah! So this function is pretty straight forward, it seems to just call `math/rng` on `os/time` which according to the documentation, seeds the `prng`. However one thing stands out right away when testing:

```clojure
repl:3:> (os/time)
1688359303
repl:4:> (os/time)
1688359304
repl:5:> (os/time)
1688359304
repl:6:> (os/time)
1688359305
repl:7:> (os/time)
1688359305
repl:8:> (os/time)
1688359305
repl:9:> (os/time)
1688359305
repl:10:> (os/time)
1688359306
```

`os/time` returns epoch time with precision to the `seconds`!. With this final detail, its pretty clear that we can predict `(os/time)` which therefore we can then seed the `prng`. Since the game will only generate the seed once and the values once, we have 5 guesses to guess the exact `(os/time)` used on the server, and with that we can get the results of `(random-float)`.

First, here is my implementation of the `program/random-float` method since I was unable to call the program's one directly.

```clojure
(defn get-random-float [min max core]
  (+ min (* (- max min) (math/rng-uniform core))))
```

I then wrote a janet script to print 5 possible values in the order of the programs function calls, to get possible lat and long values used.

```clojure
(def l (os/time)) # get time once at beginning

(def t (+ l 4)) # base offset

# test 5 different seeds 
(def c1 (math/rng (- t 3))) 
(def c2 (math/rng (- t 2)))
(def c3 (math/rng (- t 1)))
(def c4 (math/rng (- t 0)))
(def c5 (math/rng (- t -1)))

(defn get-random-float [min max core]
  (+ min (* (- max min) (math/rng-uniform core))))

# print each random float possibility with each seed
(def f1 (get-random-float -90 90 c5))
(def f2 (get-random-float -180 180 c5))
(print f1 "," f2)

(def f1 (get-random-float -90 90 c4))
(def f2 (get-random-float -180 180 c4))
(print f1 "," f2)

(def f1 (get-random-float -90 90 c3))
(def f2 (get-random-float -180 180 c3))
(print f1 "," f2)

(def f1 (get-random-float -90 90 c2))
(def f2 (get-random-float -180 180 c2))
(print f1 "," f2)

(def f1 (get-random-float -90 90 c1))
(def f2 (get-random-float -180 180 c1))
(print f1 "," f2)
```

The time offset was a bit tricky. I was surprised because it seemed like 5 seconds would be large enough window, but there was quite a difference between locally testing it and it working on remote. Regardless, I was able to just change the offset while the script was running in order to try new offsets. 

## **Solution**
```py
from pwn import *

pty = process.PTY
def solve_challenge():
    #conn = process(['./janet', '-i', 'program.jimage'], stdin=pty, stdout=pty)
    conn = remote('geoguesser.chal.uiuc.tf', 1337)
    process_output = process(['./janet', 'solve.janet']).recvall().decode().splitlines()
    print(process_output)
    response = conn.recv()
    assert len(process_output) == 5
    for i in range(5): 
        print(response)
        conn.sendline(process_output[i].encode())
        response = conn.recv()
        print(response)
        if b"You lose!" in response:
            conn.close()
            return False
        if b"uiuc" in response:
            conn.interactive()
    
    conn.close()
    return False

while True:
    if solve_challenge():
        break
```

```console
abhi@abhi-omen:~/UIUCTF/janet$ python solve.py
[+] Opening connection to geoguesser.chal.uiuc.tf on port 1337: Done
[+] Starting local process './janet': pid 6045
[+] Receiving all data: Done (84B)                                                                                             [*] Process './janet' stopped with exit code 0 (pid 6045)
['-24.6837,155.466', '-75.0369,167.254', '-45.2335,169.968', '-5.97108,136.756', '-67.0471,-79.78']
b'== proof-of-work: disabled ==\n'
b'Welcome to geoguesser!\nWhere am I? '
b'Welcome to geoguesser!\nWhere am I? '
b'You win!\nThe flag is: uiuctf{i_se3_y0uv3_f0und_7h3_t1m3_t0_r3v_th15_b333b674c1365966}\n'
[*] Switching to interactive mode
[*] Got EOF while reading in interactive
```

---
## **Flag**: uiuctf{i_se3_y0uv3_f0und_7h3_t1m3_t0_r3v_th15_b333b674c1365966}
---
