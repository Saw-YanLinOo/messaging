# server.py
import socket
import threading

# Define server address and port
SERVER_HOST = '10.29.104.169'
SERVER_PORT = 12345

# List of connected clients
clients = []


def handle_client(client_socket):
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received: {message}")
                # Broadcast message to all clients
                broadcast_message(message, client_socket)
            else:
                break
        except ConnectionResetError:
            break

    # Remove client from list and close connection
    clients.remove(client_socket)
    client_socket.close()


def broadcast_message(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except BrokenPipeError:
                clients.remove(client)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"New connection from {addr}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    start_server()
