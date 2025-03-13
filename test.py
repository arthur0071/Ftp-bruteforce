# network scanner

import socket
import os
import sys
import time
import threading

max_threads = 50
semaphore = threading.Semaphore(max_threads)

if len(sys.argv) != 3:
    print("Usage: python test.py <ip> <timeout>")
    sys.exit(1)

ip = sys.argv[1]
timeout = int(sys.argv[2])

def port_scan(host, port, timeout):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        if s.connect_ex((host, int(port))) == 0:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} [+] Port {port} [TCP] is open")
        s.close()
    except Exception as e:
        print(f"Exception: {e}")

