# Python Terminal-Based Chat Application

## Table of Contents

1. [Project Description](#project-description)
2. [Features](#features)
3. [Project Scope](#project-scope)
4. [Requirements](#requirements)
5. [Setup Instructions](#setup-instructions)
   - [1. Clone the Repository](#1-clone-the-repository)
   - [2. Install Required Libraries](#2-install-required-libraries)
   - [3. (Optional) Set Up a Virtual Environment](#3-optional-set-up-a-virtual-environment)
6. [Running the Application](#running-the-application)
   - [1. Running the Server](#1-running-the-server)
   - [2. Running the Client](#2-running-the-client)
   - [3. Testing Across Different Machines](#3-testing-across-different-machines)
7. [Code Structure](#code-structure)
   - [Server (`server.py`)](#server-serverpy)
   - [Client (`client.py`)](#client-clientpy)
   <!-- 8. [Challenges and Solutions](#challenges-and-solutions) -->
8. [How to Use the Application](#how-to-use-the-application)
<!-- 10. [Presentation Preparation](#presentation-preparation) -->
9. [Submission](#submission)
10. [Additional Resources](#additional-resources)

---

## Project Description

This project is a **Python terminal-based chat application** that enables multiple users to communicate over a local network in real-time. It consists of a **server** that manages connections and broadcasts messages, and **clients** that connect to the server to send and receive messages. The application leverages **socket programming**, **multithreading**, and the **colorama** library to enhance user experience with colored terminal outputs.

---

## Features

- **Real-Time Messaging:** Enables instantaneous communication between multiple clients.
- **Client-Server Architecture:** Centralized server manages client connections and message broadcasting.
- **Multithreading:** Supports concurrent handling of multiple clients without performance degradation.
- **Color-Coded Output:** Utilizes `colorama` to differentiate between server messages, client messages, and system notifications.
- **Graceful Exit:** Allows users to exit the chat gracefully by typing `exit`.

---

## Project Scope

This project demonstrates intermediate-level Python programming skills, including:

- **Socket Programming:** Establishing and managing network connections.
- **Multithreading:** Handling multiple client connections simultaneously.
- **User Interface Enhancement:** Improving terminal output readability with colored text.

---

## Requirements

- **Python 3.x**
- **colorama** library for colored terminal output

---

## Setup Instructions

### 1. Clone the Repository

Clone the project repository to your local machine using Git:

```bash
git clone https://github.com/Saw-YanLinOo/terminal-chat-application.git
cd terminal-chat-application
```

### 2. Install Required Libraries

Install the necessary Python libraries using `pip`:

```bash
pip install colorama
```

_If you have multiple versions of Python installed, you might need to use `pip3` instead:_

```bash
pip3 install colorama
```

### 3. (Optional) Set Up a Virtual Environment

Creating a virtual environment is recommended to manage dependencies effectively.

1. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**

   - On **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```

   - On **Windows**:

     ```bash
     venv\Scripts\activate
     ```

3. **Install Dependencies within the Virtual Environment**

   ```bash
   python3 -m pip install colorama
   ```

_Remember to activate the virtual environment each time you work on the project._

---

## Running the Application

### 1. Running the Server

1. **Open a Terminal on the Server Machine.**
2. **Navigate to the Project Directory.**
3. **Run the Server Script:**

   ```bash
   python server.py
   ```

   _The server will start and listen for incoming client connections._

### 2. Running the Client

1. **Obtain the Server’s IP Address:**

   - **On Windows:**

     ```bash
     ipconfig
     ```

   - **On macOS/Linux:**

     ```bash
     ifconfig
     ```

   _Identify the local IP address, e.g., `192.168.1.5`._

2. **Modify the Client Code:**

   Open `client.py` in a text editor and set the `SERVER_HOST` variable to the server’s IP address:

   ```python
   SERVER_HOST = '192.168.1.5'  # Replace with your server's local IP
   SERVER_PORT = 12345
   ```

3. **Run the Client Script:**

   ```bash
   python client.py
   ```

   _The client will connect to the server, allowing the user to send and receive messages._

### 3. Testing Across Different Machines

Ensure both the server and client machines are connected to the same local network (e.g., same Wi-Fi or LAN).

1. **Start the Server on the Host Machine.**
2. **Start the Client on Another Machine:**

   - Ensure the `SERVER_HOST` in `client.py` is correctly set to the server’s IP.
   - Run the client script as described above.

3. **Send Messages:**
   - Clients can send messages that will be broadcast to all connected clients.
   - Observe the color-coded output enhancing readability.

---

## Code Structure

### Server (`server.py`)

```python
# server.py
import socket
import threading
from colorama import init, Fore

# Initialize colorama
init()

# Define server address and port
SERVER_HOST = 'localhost'  # Listen on all available interfaces
SERVER_PORT = 12345

clients = []

def handle_client(client_socket):
    """Handles communication with a connected client."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{Fore.GREEN}Received: {message}{Fore.RESET}")
                if message.lower() == 'exit':
                    print(f"{Fore.RED}Client disconnected{Fore.RESET}")
                    break
                broadcast_message(message, client_socket)
            else:
                break
        except ConnectionResetError:
            break

    clients.remove(client_socket)
    client_socket.close()

def broadcast_message(message, sender_socket):
    """Sends the message to all clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except BrokenPipeError:
                clients.remove(client)

def start_server():
    """Sets up the server and starts listening for incoming connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()
    print(f"{Fore.YELLOW}Server started on {SERVER_HOST}:{SERVER_PORT}{Fore.RESET}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"{Fore.CYAN}New connection from {addr}{Fore.RESET}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
```

### Client (`client.py`)

```python
# client.py
import socket
import threading
from colorama import init, Fore

# Initialize colorama
init()

# Define server address and port
SERVER_HOST = 'localhost'  # Replace with your server's local IP
SERVER_PORT = 12345

def receive_messages(client_socket):
    """Continuously listens for messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{Fore.BLUE}{message}{Fore.RESET}\n")
                if message.lower() == 'exit':
                    print(f"{Fore.RED}Server has disconnected{Fore.RESET}")
                    break
            else:
                break
        except ConnectionResetError:
            break

def start_client():
    """Connects to the server and handles sending and receiving messages."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    while True:
        message = input()
        if message:
            client_socket.send(message.encode('utf-8'))
            if message.lower() == 'exit':
                print(f"{Fore.RED}Exiting...{Fore.RESET}")
                break

    client_socket.close()

if __name__ == "__main__":
    start_client()
```

---

<!-- ## Challenges and Solutions

### 1. Managing Multiple Client Connections

**Challenge:** Handling simultaneous connections from multiple clients without blocking the server.

**Solution:** Implemented **multithreading**, where each client connection is managed in a separate thread. This allows the server to handle multiple clients concurrently without performance issues.

### 2. Broadcasting Messages Efficiently

**Challenge:** Ensuring that messages from one client are reliably sent to all other connected clients.

**Solution:** Created a `broadcast_message` function that iterates through the list of connected clients and sends the message to each client except the sender. This ensures all participants receive the messages in real-time.

### 3. Handling Client Disconnections

**Challenge:** Preventing server crashes when a client disconnects unexpectedly.

**Solution:** Added **exception handling** using `try-except` blocks to catch `ConnectionResetError` and other potential exceptions. This allows the server to remove disconnected clients gracefully without affecting other active connections.

### 4. Enhancing User Experience with Colored Output

**Challenge:** Differentiating between server messages, client messages, and system notifications in the terminal.

**Solution:** Utilized the **`colorama`** library to apply different colors to various types of messages. This improves readability and provides a better user experience by visually distinguishing different message sources.

--- -->

## How to Use the Application

### Sending Messages

1. **Connect to the Server:**

   - Run the client script on your machine.
   - Ensure the `SERVER_HOST` is correctly set to the server’s IP address.

2. **Type Your Message:**
   - Enter your message in the terminal and press `Enter`.
   - The message will be sent to the server and broadcasted to all other connected clients.

### Exiting the Chat

- **Graceful Exit:**
  - Type `exit` and press `Enter`.
  - The client will disconnect from the server, and the server will remove the client from its active list.

---

<!-- ## Presentation Preparation

### Demonstration

- **Server Setup:**
  - Show the server terminal running and listening for connections.
- **Client Connections:**
  - Connect multiple clients from different machines on the same network.
- **Real-Time Messaging:**
  - Send messages from one client and display them on all connected clients’ terminals.
- **Exiting:**
  - Demonstrate how clients can exit the chat gracefully by typing `exit`.

### Discussion Points

- **Code Structure:**
  - Explain the separation between server and client scripts.
- **Design Choices:**
  - Discuss the use of multithreading for handling multiple clients.
  - Explain the integration of `colorama` for enhancing terminal output.
- **Challenges Faced:**
  - Elaborate on the challenges encountered during development and how they were resolved, such as managing client disconnections and ensuring message broadcasting efficiency.

### Q&A Preparation

Be ready to answer questions related to:

- **Socket Programming:**
  - How sockets establish connections between server and clients.
- **Threading:**
  - How threads are used to handle multiple clients.
- **Error Handling:**
  - Techniques used to manage exceptions and maintain application stability.
- **Libraries Used:**
  - The role and benefits of using `colorama` for colored outputs.

--- -->

## Submission

### Files to Include

- `server.py`: Server-side script handling client connections and message broadcasting.
- `client.py`: Client-side script for connecting to the server and sending/receiving messages.
- `README.md`: Comprehensive documentation of the project.

### Directory Structure

Ensure your project directory is well-organized:

```
chat-application/
├── server.py
├── client.py
├── README.md
└── (Optional) other resources
```

<!-- ### Submission Method

Submit your project via the preferred submission platform (e.g., GitHub repository link, zip file upload) by the specified deadline. Ensure all files are included and organized as per the guidelines. -->

---

## Additional Resources

- **colorama Documentation:** [https://pypi.org/project/colorama/](https://pypi.org/project/colorama/)
- **Python Socket Programming:** [https://docs.python.org/3/library/socket.html](https://docs.python.org/3/library/socket.html)
- **Python Threading:** [https://docs.python.org/3/library/threading.html](https://docs.python.org/3/library/threading.html)
- **Creating Virtual Environments:** [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)

---

## Acknowledgements

- Inspired by various online resources, including tutorials and open-source projects.
- Special thanks to Asst. Prof. Sa-nga Songmuang for the support.

---

Feel free to ask me any additional features or specific requirements of this project.
