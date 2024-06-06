#!/usr/bin/env python3

import threading
import socket
import queue
from tkinter import *
from tkinter.scrolledtext import ScrolledText

def send_message(client_soket, username, text_widget, entry_widget):
    message = entry_widget.get()
    client_soket.sendall(f"{username} > {message}".encode())

    entry_widget.delete(0, END)
    text_widget.configure(state='normal')
    text_widget.insert(END, f"{username} > {message}\n")
    text_widget.configure(state='disable')

def receive_message(client_soket, text_queue):
    while True:
        try:
            message = client_soket.recv(1024).decode()
            print(message)
            if not message:
                break
            
            text_queue.put(message)
        except:
            break

def update_text_widget(text_widget, text_queue):
    while not text_queue.empty():
        message = text_queue.get()
        text_widget.configure(state='normal')
        text_widget.insert(END, message +"\n")
        text_widget.configure(state='disable')
    text_widget.after(100, update_text_widget, text_widget, text_queue)


def list_users_request(client_soket):
    client_soket.sendall("!usuarios".encode())

def exit_request(client_soket, username, window):

    client_soket.sendall(f"\n El usuario {username} ha abandonado el chat\n".encode())
    client_soket.close()

    window.quit()
    window.destroy()

def client_program():

    host = 'localhost'
    port = 12345

    client_soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_soket.connect((host, port))


    username = input(f"\n Introduce tu usuario: ")
    client_soket.sendall(username.encode())

    window = Tk()
    window.title("Simple Chat")
    
    text_widget = ScrolledText(window, state='disable')
    text_widget.pack(padx=5, pady=5)

    frame_widget = Frame(window)
    frame_widget.pack(padx=5, pady=2, fill=BOTH, expand=1)

    entry_widget = Entry(frame_widget, font=("Arial", 14))
    entry_widget.bind("<Return>", lambda _: send_message(client_soket, username, text_widget, entry_widget))
    entry_widget.pack(side=LEFT, fill=X, expand=1)

    button_widget = Button(frame_widget, text="Enviar", command= lambda: send_message(client_soket, username, text_widget, entry_widget))
    button_widget.pack(padx=5, pady=5)

    users_widget = Button(window, text="Listar usuarios", command=lambda: list_users_request(client_soket))
    users_widget.pack(padx=5, pady=5)

    exit_widget = Button(window, text="Salir", command=lambda: exit_request(client_soket, username, window))
    exit_widget.pack(padx=5,pady=5)

    text_queue = queue.Queue()
    thread = threading.Thread(target=receive_message, args=(client_soket, text_queue))
    thread.daemon = True
    thread.start()

    update_text_widget(text_widget, text_queue)

    window.mainloop()
    client_soket.close()


if __name__ == '__main__':
    client_program()

