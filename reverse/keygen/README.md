![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&width=435&size=35&lines=Keygen)

![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&pause=1000&color=F70000&width=435&lines=Reverse)

In this challenge we are privided with keygenme-trial.py file, which contain some python code that checks our license which is the flag.

We start this challenge by reading thro the file and understanding how it works, we can see in the first few 
lines that the flag is a combination of :
```py
key_part_static1_trial = "picoCTF{1n_7h3_|<3y_of_"
key_part_dynamic1_trial = "xxxxxxxx"
key_part_static2_trial = "}"
key_full_template_trial = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial

```

So we can assume that our task is to find the `xx...` values to get the flag.

A little bit of reading will get us into this function :
```py
def check_key(key, username_trial):

    global key_full_template_trial

    if len(key) != len(key_full_template_trial):
        return False
    else:
        # Check static base key part --v
        i = 0
        for c in key_part_static1_trial:
            if key[i] != c:
                return False

            i += 1

        # TODO : test performance on toolbox container
        # Check dynamic part --v
        if key[i] != hashlib.sha256(username_trial).hexdigest()[4]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[5]:
            return False
        else:picoCTF{1n_7h3_|<3y_of_09820d0}

            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[3]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[6]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[2]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[7]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[1]:
            return False
        else:
            i += 1

        if key[i] != hashlib.sha256(username_trial).hexdigest()[8]:
            return False



        return True
```
We can see here that our `x`s are being compared with this hash charachter, and as long as we can get into this part of the code, we can print it, so this is why I did, I gave `picoCTF{1n_7h3_|<3y_of_xxxxxxxx}` as a fake license to get there and I printed the flag before this hash comparaison, and I got the flag:
```py
        flag = key_part_static1_trial
        flag = flag + hashlib.sha256(username_trial).hexdigest()[4]
        flag = flag + hashlib.sha256(username_trial).hexdigest()[5]
        flag = flag + hashlib.sha256(username_trial).hexdigest()[3]
        flag = flag + hashlib.sha256(username_trial).hexdigest()[6]
        flag = flag + hashlib.sha256(username_trial).hexdigest()[2]
        flag = flag + hashlib.sha256(username_trial).hexdigest()[7]
        flag = flag + hashlib.sha256(username_trial).hexdigest()[1]
        flag = flag + hashlib.sha256(username_trial).hexdigest()[8]
        flag = flag + '}'
        print(flag)
```

