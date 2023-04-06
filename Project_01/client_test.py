import logging
import socket
import threading
import time
import ssl
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

logger = logging.getLogger(__name__)
FORMAT = '%(asctime)server %(name)-15.5s %(threadName)-10s %(levelname)-8s %(message)server'
logging.basicConfig(level=logging.INFO, format=FORMAT)
server = socket.socket()
list_of_clients = []
client_name = "Client1"
client_channel_port = 9994


def ping():
    # Set up AES encryption key and IV
    key = b'0123456789abcdef'
    iv = b'fedcba9876543210'

    message = client_name + ": PING"
    message = pad(str.encode(message), 16)

    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        fetch_ip_adresses()
        time.sleep(5)
        try:
            for client in list_of_clients:
                if client['ip_address'] != '' and not (client_name) in client['name']:
                    sock.connect((client['ip_address'], client_channel_port))

                    # Encrypt the message using AES
                    cipher = AES.new(key, AES.MODE_CBC, iv)
                    encrypted_message = cipher.encrypt(message)

                    sock.sendall(encrypted_message)
                    print(unpad(message, 16).decode())

                    # Receive the encrypted response from the client and decrypt it using AES
                    data = sock.recv(1024)
                    cipher = AES.new(key, AES.MODE_CBC, iv)
                    decrypted_response = unpad(cipher.decrypt(data), 16).decode()
                    print(str(decrypted_response))

        except Exception as e:
            logger.error(e)

        finally:
            time.sleep(10)


def pong():
    # Set up AES encryption key and IV
    key = b'0123456789abcdef'
    iv = b'fedcba9876543210'

    message = client_name + ": PONG"
    message = pad(str.encode(message), 16)

    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('127.0.0.1', client_channel_port))
            sock.listen(15)

            (client_socket, client_address) = sock.accept()
            data = client_socket.recv(2048)

            if data:
                # Decrypt the received message using AES
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decrypted_message = unpad(cipher.decrypt(data), 16).decode()

                print(str(decrypted_message))

                # Encrypt the response message using AES and send it back to the client
                cipher = AES.new(key, AES.MODE_CBC, iv)
                encrypted_response = cipher.encrypt(message)
                client_socket.sendall(encrypted_response)

                print(unpad(message, 16).decode())

        except socket.error as e:
            logger.error("Socket error:", e)

        finally:
            time.sleep(2)

def connect_to_server(client_name = "Client1"):
    logger.info("Connection to Server.py Thread")
    host = 'localhost'
    port2 = 9995
    global sock_ssl
    sock_ssl= ssl.wrap_socket(server, cert_reqs=ssl.CERT_REQUIRED, ca_certs='server.crt')
    sock_ssl.connect((host, port2))
    print(f"Registered with name: {client_name}")
    while True:
        sock_ssl.sendall(pad(str.encode(client_name), 16))
        time.sleep(5)

def fetch_ip_adresses(data=None):
    data=''
    while((data)==''):
        data = sock_ssl.recv(2048).decode("utf-8")
        if len(data) > 1:
            print (data)
            print(len(data))
            ips = data.strip().split(',')
            if len(ips) > 0:
                list_of_clients.clear()
                for ip in ips:
                    if len(ip) > 0:
                        print(ip)
                        client = {'name': ip.split(':')[1], 'ip_address': ip.split(':')[0]}
                        if ' ' not in client['name']:
                            list_of_clients.append(client)

            logger.info(f'Current list of clients: {(list_of_clients)}')

# # logger.info(f'spawning before')
server_thread = threading.Thread(target=connect_to_server, args=(client_name,))
server_thread.start()
time.sleep(10)
ping_thread = threading.Thread(target=ping)
pong_thread = threading.Thread(target=pong)
ping_thread.start()
pong_thread.start()