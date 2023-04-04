import socket
import time
import threading
import os
import logging
import re

logger = logging.getLogger(__name__)
FORMAT = '%(asctime)server %(name)-15.5s %(threadName)-10s %(levelname)-8s %(message)server'
logging.basicConfig(level=logging.INFO, format=FORMAT)
list_of_clients = []
server = socket.socket()
client_name = "Client1"
client_channel_port = 9994

def ping():

    message = client_name + ": PING"
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        fetch_ip_adresses()
        try:
            for client in list_of_clients:
                if client['ip_address'] != '' and not (client_name) in client['name']:
                    sock.connect((client['ip_address'], client_channel_port))
                    print(message)
                    sock.sendall(bytes(message, 'utf-8'))
                    data = sock.recv(1024)
                    print(str(client['ip_address']) + ":" + data.decode())
                    sock.close()

        except Exception as e:
            logger.info(e)

        finally:
            time.sleep(15)
            print('Ping session complete')


def pong():
    message = client_name + ": PONG"
    print("Trying to Pong")

    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', client_channel_port))
        sock.listen(10)
        (client_socket, client_address) = sock.accept()
        try:
            data = client_socket.recv(2048).decode()
            if data:
                client_socket.send(bytes(message, 'utf-8'))
                print(str(client_address) + ":" + data)
        except socket.error as e:
            print("Socket error:", e)
        finally:
            sock.close()


def connect_to_server():
    # logger.info("Connection to Server.py Thread")
    host = 'localhost'
    port2 = 9995
    server.connect((host, port2))
    print(f"Registered with name: {client_name}")
    while True:
        server.sendall(bytes(client_name, 'utf-8'))
        time.sleep(5)


def fetch_ip_adresses():
    print("Fetch ip")
    list_of_clients.clear()
    data = server.recv(2048)
    if len(data) > 0:
        data1 = str(data.decode("utf-8"))
        print("Data" + data1)
        ips = data1.strip().split(',')
        if len(ips) > 0:
            for ip in ips:
                print(ip)
                client = {'name': ip.split(':')[1], 'ip_address': ip.split(':')[0]}
                if ' ' not in client['name']:
                    list_of_clients.append(client)

        logger.info(f'Current list of clients: {(list_of_clients)}')


# connect_to_server(client_name)

# # logger.info(f'spawning before')
server_thread = threading.Thread(target=connect_to_server)
server_thread.start()
time.sleep(10)
ping_thread = threading.Thread(target=ping)
pong_thread = threading.Thread(target=pong)
ping_thread.start()
pong_thread.start()