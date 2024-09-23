import socket
import threading

def receive_messages(client_socket):
    """Receive messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            print("Connection to the server has been lost.")
            break

def start_client(username):
    """Start the client to send messages."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    client_socket.send(username.encode('utf-8'))

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    while True:
        message = input()
        if message.lower() == 'exit':
            client_socket.close()
            break
        client_socket.send(f"{username}: {message}".encode('utf-8'))

if __name__ == "__main__":
    username = input("Enter your device name: ")
    start_client(username)