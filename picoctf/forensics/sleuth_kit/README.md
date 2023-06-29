[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Sigmar&size=25&duration=3700&pause=400&width=435&lines=Sleuthkit%20Intro)](https://git.io/typing-svg)

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Sigmar&size=25&duration=3700&pause=700&color=F72424&width=435&lines=Forensics)](https://git.io/typing-svg)


![Screenshot from 2023-05-18 14-31-05](https://github.com/L3AK-TEAM/picoctf-writeups/assets/102762345/db4c6af2-0387-43eb-bf8d-d62154215a80)


### Very Easy Forensics challenge that involves disk analysis via the command line. Lets start by downloading the image from the description.


![Screenshot from 2023-05-18 14-15-40](https://github.com/L3AK-TEAM/picoctf-writeups/assets/102762345/fdba9eb0-495e-4362-9940-29cb72b2830b)


### As seen in the challenge description , we would need to use the command `mmls`. I've been using that command for quite sometime and its great. Essentially what it does is, tries to give us a nice layout of the disk partitions and their sizes. So let's get into it by trying to run it.

`mmls disk.img`

![image](https://github.com/L3AK-TEAM/picoctf-writeups/assets/102762345/874d65ef-f483-4e89-8c03-58d5bfa17f1d)

### Great, as we can see we were given the data that we were looking for. We are looking for the length of the image. So lets try submitting `0000202752` as our answer to the netcat listener.

![image](https://github.com/L3AK-TEAM/picoctf-writeups/assets/102762345/3adc07f6-1142-4159-b5af-60be2aa12612)

### Well that was easy wasnt it ? Time to move into more advanced stuff with disk forensics !

`FLAG: picoCTF{mm15_f7w!}`




