
![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&width=435&size=35&lines=Speeds+and+feeds)

![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&pause=1000&color=F70000&width=435&lines=Reverse)

For this challenge we were provided with simple a remote service.

We try to connect using netcat : `nc mercury.picoctf.net 16524`

And we get this kind of strings :

```
...
G1X149.0345Y-0.5517
G0Z0.1
...
```
I immediatly assumed that this G-code which is the code for 3D printers, so what I did, was first saving the code using : `nc mercury.picoctf.net 16524 > file.csc` and then trying to visualise in any website, I used `https://ncviewer.com/` , you upload the file and get the flag.