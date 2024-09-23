import socket
import threading

# List to hold connected clients
clients = []
usernames = []

def handle_client(client_socket):
    """Handle incoming messages from a client."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                broadcast(message, client_socket)
            else:
                remove(client_socket)
                break
        except:
            remove(client_socket)
            break

def broadcast(message, client_socket):
    """Send a message to all clients except the sender."""
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove(client)

def remove(client_socket):
    """Remove a client from the list."""
    if client_socket in clients:
        index = clients.index(client_socket)
        clients.remove(client_socket)
        username = usernames[index]
        usernames.remove(username)
        broadcast(f"{username} has left the chat.", client_socket)

def start_server():
    """Start the server to accept client connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Server started on port 12345")

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        username = client_socket.recv(1024).decode('utf-8')
        usernames.append(username)
        print(f"{username} has connected from {addr}")
        broadcast(f"{username} has joined the chat.", client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()