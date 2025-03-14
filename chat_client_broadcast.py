import socket
import threading

# Configuration
PORT = 12345  # TCP port for chat
BROADCAST_PORT = 50000  # UDP broadcast port
BUFFER_SIZE = 1024

# Function to listen for server broadcast and get the server's IP
def discover_server():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.bind(("", BROADCAST_PORT))

    print(f"Listening for server broadcasts on UDP port {BROADCAST_PORT}...")
    while True:
        data, addr = udp_socket.recvfrom(BUFFER_SIZE)
        message = data.decode()
        if ":" in message:
            server_ip, port = message.split(":")
            print(f"Discovered server at {server_ip}:{port}")
            return server_ip, int(port)

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode()
            print(message)
        except:
            print("Connection lost.")
            client_socket.close()
            break

# Discover the server
server_ip, server_port = discover_server()

# Create a TCP socket and connect to the discovered server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Start a thread to receive messages
threading.Thread(target=receive_messages, daemon=True, args=(client_socket,)).start()

# Main chat loop
while True:
    message = input()
    if message.lower() == "exit":
        client_socket.send("exit".encode())
        break
    client_socket.send(message.encode())

client_socket.close()
