# client.py
import socket
import threading
from colorama import init, Fore


# Initialize colorama
init()

# Define server address and port
SERVER_HOST = '10.29.104.169'
SERVER_PORT = 12345

# User Name
name = ""


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"\n{Fore.GREEN}{message}{Fore.RESET}\n")
                # print(f"\n{message}")
            else:
                break
        except ConnectionResetError:
            break
        except KeyboardInterrupt:
            break
        except OSError:
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    name = input("Enter your name : ")
    if name:
        client_socket.send((name+" join the club.").encode('utf-8'))
    while True:
        message = input()
        if message:
            client_socket.send(("["+name+"] "+message).encode('utf-8'))
            if message.lower() == 'exit':
                break

    client_socket.close()


if __name__ == "__main__":
    start_client()
