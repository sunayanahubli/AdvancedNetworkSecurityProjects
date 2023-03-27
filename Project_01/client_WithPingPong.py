import socket
import time
import threading
import os

def pong(ip_address, port):
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip_address, port))
        sock.listen(100)
        connection, client_address = sock.accept()
        try:
            # print('connection from', client_address)
            data = connection.recv(16)
            print('received "%s"' % data.decode())
            if data:
                # print('sending data back to the client')
                connection.sendall(b'Pong')
            else:
                break

        finally:
            # print('Cleanup')
            connection.close()

def ping(ip_address, port):
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect the socket to the server's address and port
            server_address = (ip_address, port)
            # print('connecting to %s port %s' % server_address)
            sock.connect(server_address)

            # Send data
            message = b"PING"
            # print('sending "%s"' % message)
            sock.sendall(message)

            data = sock.recv(16)
            print('received "%s"' % data.decode())

        except Exception as e:
            print(e)

        finally:
            # print('closing socket')
            sock.close()


def connect_to_server():
    global list_of_ip
    while True:
        list_of_ip=''
        print("Connection to Server Thread")
        s = socket.socket()
        host = '192.168.1.50'
        port2 = 9996
        s.connect((host, port2))

        data = s.recv(1024)
        if data[:2].decode("utf-8") == 'cd':
                os.chdir(data[3:].decode("utf-8"))

        if len(data) > 0:
            print(data.decode("utf-8"))
            list_of_ip=(str(data.decode("utf-8")))

            time.sleep(15)

conn_thread = threading.Thread(target=connect_to_server)
port1 = 9998
conn_thread.start()
time.sleep(15)
ping_thread = threading.Thread(target=ping, args=(list_of_ip, port1))
pong_thread = threading.Thread(target=pong, args=(list_of_ip, port1))
ping_thread.start()
pong_thread.start()
