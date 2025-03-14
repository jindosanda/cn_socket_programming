import socket
import threading

# Configuration
PORT = 12345  # TCP port for chat
BROADCAST_PORT = 50000  # UDP port for broadcasting the server IP
BROADCAST_INTERVAL = 5  # Seconds between broadcasts

clients = {}  # Dictionary to store connected clients

def broadcast_server_ip():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    server_ip = get_local_ip()  # Get the correct LAN IP
    message = f"{server_ip}:{PORT}"
    
    while True:
        udp_socket.sendto(message.encode(), ("<broadcast>", BROADCAST_PORT))
        print(f"Broadcasting server IP {server_ip} on UDP port {BROADCAST_PORT}")
        threading.Event().wait(BROADCAST_INTERVAL)


# Function to handle a client connection
def handle_client(client_socket):
    try:
        client_socket.send("Enter your username: ".encode())
        username = client_socket.recv(1024).decode().strip()
        if not username:
            client_socket.close()
            return
        
        clients[client_socket] = username
        print(f"{username} connected.")
        broadcast(f"{username} joined the chat.")

        while True:
            message = client_socket.recv(1024).decode()
            if message.lower() == "exit":
                break
            broadcast(f"{username}: {message}", sender_socket=client_socket)
    
    except:
        pass  # Handle errors gracefully

    remove_client(client_socket)

# Function to broadcast a message to all clients
def broadcast(message, sender_socket=None):
    for client_socket in list(clients.keys()):
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except:
                remove_client(client_socket)

# Function to remove a disconnected client
def remove_client(client_socket):
    if client_socket in clients:
        username = clients[client_socket]
        print(f"{username} disconnected.")
        del clients[client_socket]
        client_socket.close()
        broadcast(f"{username} left the chat.")

# Main TCP server function
def start_tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", PORT))  # Listen on all network interfaces
    server_socket.listen()
    print(f"Server listening on all interfaces, port {PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def get_local_ip():
    """Returns the actual LAN IP of the server."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to an external address (doesn't send data, just used for IP detection)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()
    return local_ip


# Start both the UDP broadcaster and the TCP server
if __name__ == "__main__":
    threading.Thread(target=broadcast_server_ip, daemon=True).start()
    start_tcp_server()
