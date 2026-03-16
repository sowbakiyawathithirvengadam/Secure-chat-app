import socket
import threading

HOST = "127.0.0.1"
PORT = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
names = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass

def handle(client):

    while True:
        try:
            message = client.recv(200000)
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)

            name = names[index]
            names.remove(name)

            broadcast(f"{name} left the chat".encode())

            client.close()
            break

def receive():

    print("Server started...")

    while True:

        client, address = server.accept()

        client.send("NAME".encode())

        name = client.recv(1024).decode()

        names.append(name)
        clients.append(client)

        print(name, "connected")

        broadcast(f"{name} joined the chat".encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()