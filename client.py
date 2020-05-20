import socket
from _thread import start_new_thread


def get_data():
    global running, z
    while running:
        data = z.recv(1024).decode()
        if data == '0':
            running = False
            z.close()
        else:
            print(data)


def send_data():
    global running, z
    while True:
        data = input()
        z.send(data.encode())
        if data == '0':
            running = False
            z.close()
            break


print("Enter message to others others:")
running = True
host = "192.168.1.105"
port = 8016
z = socket.socket()
z.connect((host, port))
start_new_thread(get_data, ())
send_data()