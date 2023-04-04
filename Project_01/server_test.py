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
results_withname=[]

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

def accepting_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_address[:]

    while True:
        client = {}
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            # print("Connection has been established :" + address[0])
            data = conn.recv(1024)
            client['name'] = data.decode()
            client['addr']= address[0]
            client['con']= conn
            results_withname.append(client)
            print('Client Registered with name "%s"' % client['name'])
            print(client)
        except:
            print("Error accepting connections")


def list_connections():
     results.clear()
     # for i, conn in enumerate(all_connections):
     #        try:
     #            print('Attempting to send string')
     #            conn.send(str.encode(' '))
     #            print('sent string')
     #            print('recv string')
     #            results.append((all_address[i])[0])
     #            print((all_address[i])[0])
     #        except:
     #            print('Exception')
     #            del all_connections[i]
     #            del all_address[i]
     #            continue
     for i, conn in enumerate(results_withname):
         try:
             # print('Attempting to send string')
             # print(conn['con'])
             (conn['con']).send(str.encode(' '))
             # print('sent string')
             # print('recv string')
             # results.append((all_address[i])[0])
             # print((all_address[i])[0])
         except:
             print('Exception')
             del all_connections[i]
             del all_address[i]
             del results_withname[i]
             continue
     # print(results_withname)

def send_list_connections():
    while True:
        time.sleep(10)
        list_connections()
        dummy = []
        for conn in results_withname:
            print("Sending list")
            dummy.append((conn['addr'] + ":" + conn['name']))
        for client in results_withname:
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