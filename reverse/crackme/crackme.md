![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&width=435&size=35&lines=Crackme)

![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&pause=1000&color=F70000&width=435&lines=Reverse)

In this challenge we were provided with a python script again.

After reading the content of the file, we find an interesting variable `bezos_cc_secret` which we can understand from the comments that it shouldn't be there, and in addition of that we have a function `decode_secret` which is meant to decode something, so as a first reflex, I called the function with the secret as an argument in the beginning of our flow, and I got the flag.

```py
decode_secret(bezos_cc_secret)
```

