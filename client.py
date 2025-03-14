import socket
import threading

# Configuration
SERVER_IP = "192.168.1.50"  # Change this to the actual server's IP address
PORT = 12345

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()  # Receive and decode message
            if not message:
                break  # Exit if the server closes the connection
            print(message)
        except:
            print("Connection lost.")
            client_socket.close()
            break

# Start a background thread to listen for incoming messages
threading.Thread(target=receive_messages, daemon=True).start()

# # Prompt the user for a username and send it to the server
# username = input("Enter your username: ")
# client_socket.send(username.encode())

# Loop to send messages to the server
while True:
    message = input()
    if message.lower() == "exit":  # If user types 'exit', close the connection
        client_socket.send("exit".encode())
        break
    client_socket.send(message.encode())  # Send the message to the server

client_socket.close()  # Close the connection when done
