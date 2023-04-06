import socket
import threading
import time
from queue import Queue
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from json import dumps, loads
from requests import post as post_request
import ssl
import certifi

NUMBER_OF_THREADS = 3
JOB_NUMBER = [1, 2, 3]
queue = Queue()
all_connections = []
all_address = []
results=[]

# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9995
        s = socket.socket()


    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(15)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()

# def accepting_connections():
#     for c in all_connections:
#         c.close()
#     del all_connections[:]
#     del all_address[:]
#
#     while True:
#             client = {}
#         # try:
#             conn, address = s.accept()
#             s.setblocking(1)  # prevents timeout
#
#             all_connections.append(conn)
#             all_address.append(address)
#             data = conn.recv(1024)
#             client['name'] = unpad(data,16).decode()
#             client['addr']= address[0]
#             client['con']= conn
#             results.append(client)
#             print('Client Registered with name "%s"' % client['name'])
#             print(client)
#         # except:
#         #      print("Error accepting connections")

def accepting_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_address[:]
    sock_ssl = ssl.wrap_socket(s, server_side=True, certfile='server.crt', keyfile='server.key')
    sock_ssl.listen()

    while True:
        client = {}
        try:
            conn, address = sock_ssl.accept()
            sock_ssl.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)
            data = conn.recv(2048)
            if len(data) % 16 != 0:
                print(len(data) )
                continue
            client['name'] = unpad(data, 16).decode()
            client['addr'] = address[0]
            client['con'] = conn
            results.append(client)
            print('Client Registered with name "%s"' % client['name'])
            print(client)
        except Exception as e:
            print("Error accepting connections:", e)

def list_connections():
     for i, conn in enumerate(results):
         try:
             (conn['con']).send(str.encode(' '))
         except:
             print('Exception')
             # del all_connections[i]
             # del all_address[i]
             # del results[i]
             continue

def send_list_connections():
    while True:
        time.sleep(5)
        list_connections()
        dummy = []
        for conn in results:
            print("Sending list")
            dummy.append((conn['addr'] + ":" + conn['name']))
        for client in results:
            b= ','.join(dummy)
            (client['con']).send(str.encode(b))
            print( client['con'])
            print(b)
        print("Sending List Done")

# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            pass
        if x == 3:
            send_list_connections()
        queue.task_done()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()

create_workers()

create_jobs()

