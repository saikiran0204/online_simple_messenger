from socket import *
from _thread import start_new_thread


def send_message(msg, index):
    global connection_list
    for i in range(len(connection_list)):
        if connection_list[i] is not None and i != index:
            connection_list[i].send(msg.encode())


def server_process(conn, index):
    global address_list, connection_list, running, names
    conn.send("Enter your name:".encode())
    name = conn.recv(1023).decode()
    if name != '':
        names[index] = name
        send_message(name + " connected", index)

    connection_list[index] = conn

    while running[index]:
        data = conn.recv(1024).decode()
        print(data)
        if data == '0':
            connection_list[index].close()
            connection_list[index] = None
            print("closed")
            running[index] = False
            send_message(name+ " disconnected", index)
        else:
            msg = str(data) + " From " + names[index]
            send_message(msg, index)


def exit_fom_process():
    global z, running, running_1
    input()
    for i in range(len(running)):
        running[i] = False
        if connection_list[i] is not None:
            connection_list[i].close()
    z.close()
    running_1 = False


z = socket()
host = "192.168.1.105"
port = 8016
z.bind((host, port))
z.listen(1)
connection_list, address_list, running, names = [], [], [], []
i = 0
start_new_thread(exit_fom_process, ())
running_1 = True
while running_1:
    connection, address = z.accept()
    address_list.append(address)
    connection_list.append(None)
    running.append(True)
    names.append("")
    k = start_new_thread(server_process, (connection, i))
    i += 1
