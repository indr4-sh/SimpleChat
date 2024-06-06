#!/usr/bin/env python3

import socket
import threading

def client_thread(client_socket, clients, usernames):

    username = client_socket.recv(1024).decode()
    usernames[client_socket] = username

    print(f"\n El usuario {username} se ha conectado al chat")

    for client in clients:
        if client is not client_socket:
            client.sendall(f"\n El usuario {username} ha entrado al chat\n".encode())

    while True:
        try:
            message = client_socket.recv(1024)

            if not message:
                break
            if message.decode() == "!usuarios":
                client_socket.sendall(f"Listando usuarios: {', '.join(usernames.values())}\n".encode())
                continue

            for client in clients:
                if client is not client_socket:
                    client.sendall(message)
        except:
            break
    client_socket.close()
    clients.remove(client_socket)
    del usernames[client_socket]

def server_program():

    host = 'localhost'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # para no dejar colgando el hitlo TIME_WAIT
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("\nEl servidor esta escuchando nuevas conexiones...")

    clients = []
    usernames = {}

    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)

        print(f"\n Se ha conectado un nuevo cliente {address}")

        thread = threading.Thread(target=client_thread, args=(client_socket, clients, usernames))
        thread.daemon = True
        thread.start()

    server_socket.close()


if __name__ == '__main__':
    server_program()



