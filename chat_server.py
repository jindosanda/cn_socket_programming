import socket
import threading

# Server configuration
HOST = "0.0.0.0"  # Listen on all network interfaces
PORT = 12345       # Port to listen on

# Creazione del socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}...")

clients = {}  # Dictionary to store connected clients

# Functin to broadcast a message to all connected clients
def broadcast(message, sender_socket=None):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except:
                # Remove the client if it's no longer active
                remove_client(client_socket)

# Remove the client from the list of clients
def remove_client(client_socket):
    if client_socket in clients:
        username = clients[client_socket]
        print(f"{username} disconnected.")
        del clients[client_socket]
        client_socket.close()
        broadcast(f"{username} left the chat.")

# Manage a single client
def handle_client(client_socket):
    try:
        # Chiede l'username al client
        client_socket.send("Insert your username: ".encode())
        username = client_socket.recv(1024).decode().strip()
        
        if not username:
            client_socket.close()
            return
        
        print(f"{username} connected.")
        clients[client_socket] = username
        broadcast(f"{username} joined the chat.")

        # Receive and broadcast messages from the client
        while True:
            message = client_socket.recv(1024).decode()
            if message.lower() == "exit":
                break
            broadcast(f"{username}: {message}", sender_socket=client_socket)
    
    except:
        pass  # Hanlde Network I/O error

    # Disconnessione del client
    remove_client(client_socket)

# Accept new connections
while True:
    client_socket, client_address = server_socket.accept()
    print(f"New connection from {client_address}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()
