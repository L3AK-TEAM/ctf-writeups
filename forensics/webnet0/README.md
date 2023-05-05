
[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Sigmar&size=25&duration=3700&pause=400&width=435&lines=WebNet0)](https://git.io/typing-svg)

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Sigmar&size=25&duration=3700&pause=700&color=F72424&width=435&lines=Forensics)](https://git.io/typing-svg)

![image](https://user-images.githubusercontent.com/102762345/236415637-cf77ef56-92fb-464b-a16b-6b857fc0343c.png)


This specific challenge was definetely where one can learn a lot from ! By reading the description we can tell that its going to be related to a packet capture traffic, as well as some sort of key. 

![image](https://user-images.githubusercontent.com/102762345/236415753-06f7c96b-3fd2-4384-8e55-c7522b97d31f.png)


As we can see we got 2 files which are `capture.pcap` and `picopico.key`.

Lets open that packet capture up in **wireshark** !

Can be done with `wireshark capture.pcap`, if you are using Linux **:)**

add encrypted image of packets 

add protocol hierarchy

Few things to note there, is that the traffic seems to be encrypted with *Transport Layer Security (**TLS**)*. After looking at the port numbers we see its 443 **HTTPS** which is an encrypted form of HTTP. 

If we try to follow the TCP stream we wont get anywhere at all ! So now our next step should be trying to decrypt the traffic with that **.key** file we got earlier.

This can be done by loading our RSA key in. Which can be achieved by going to `Edit --> Preferences --> RSA Keys`

add 2 images on how this can be achieved.

Okay great we got our key in. Now its time to reload our `.pcap` and see what happened.

add image of decrypted traffic.

We see that https packets got decrypted properly , lets view them in HTTP Stream now !

add http stream 

Amazing , by observing the headers we see that one of the headers names is Pico-Flag and right beside it is our flag for this challenge.

``FLAG: picoCTF{nongshim.shrimp.crackers}``


