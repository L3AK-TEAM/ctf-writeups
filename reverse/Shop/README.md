![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&width=435&size=35&lines=Shop)

![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&pause=1000&color=F70000&width=435&lines=Reverse)

For this challenge we were given, a 32bit executable and a remote instance.
As a first reaction, I connected to the instance and was playing around it.
After some time, I assumed that the goal of this challenge is to print the `Fruitful Flag`. However, to print this we have to somehow have 100 coins, when we only have 40, now after understanding the goal. I fired my ghidra and started looking into the binary (Some commun beginner mistakes, is booting ghidra immediatly. First try to understand what is the task. It's gonna make your life much easier) So in ghidra, I took a look into the code, and I found that the negative numbers aren't handled correctly, when calculating the payback after you buy something.With this fining, I went back to the remote instance, and tried it with the `Average Apple`, and unstead of buying 1 or 2 I bought -100. And ended up `1540` coins. Cool huh ? So yeah now that we satisfy the condition, I tried again to buy the flag and got this :
```
Flag is:  [112 105 99 ... 125]

```
Hmm, looks like ascii to me, so yeah, I opened `cyberchef` and chose from decimal and we got the flag.
