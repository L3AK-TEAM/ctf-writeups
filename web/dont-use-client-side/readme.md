![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&width=435&size=35&lines=dont-use-client-side)
<br>
![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&pause=1000&color=F70000&width=435&lines=Web+Exploitation)
![Challenge Description](dont-use-client-side.png)

The dont-use-client-side Challenge
![file command](index.png)

</br>
By examining the source code, we can clearly observe a section of the flag.
</br>

![file command](js.png)

</br>
`pico` | `CTF{` | `a3c8` | `ts_p` | `lien` | `lz_1` | `no_c` | `9}`
</br>
Let's generate a flag by combining these parts.
</br>
`picoCTF{no_clients_plz_1a3c89}`
</br>

`curl -s https://jupiter.challenges.picoctf.org/problem/37821/ | awk -F "'" '/if /{print $2}' | tr '\n' ' ' | awk '{print $1 $3 $7 $5 $4 $6 $2 $8}'
`
## flag
picoCTF{no_clients_plz_1a3c89}
