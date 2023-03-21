import socket
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 3
JOB_NUMBER = [1, 2, 3]
queue = Queue()
all_connections = []
all_address = []
results = []

# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9996
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

def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")

def start_turtle():

    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
        # elif 'send' in cmd:
        else:
            print("Command not recognized")

def list_connections():
     results.clear()
     for i, conn in enumerate(all_connections):
            try:
                print('Attempting to send string')
                conn.send(str.encode(' '))
                print('sent string')
                print('recv string')
                results.append((all_address[i])[0])
                # print(type(all_address[i]))
                print((all_address[i])[0])
            except:
                print('Exception')
                del all_connections[i]
                del all_address[i]
                continue
     print(results)

def send_list_connections():
    while True:
        time.sleep(10)
        list_connections()
        for conn in all_connections:
            print("Sending list")
            conn.send(str.encode((','.join(results))))
            # client_response = str(conn.recv(20480), "utf-8")
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
            # list_connections()
        if x == 2:
            start_turtle()
        if x == 3:
            send_list_connections()
        queue.task_done()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()

create_workers()
create_jobs()