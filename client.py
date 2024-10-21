import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print("Received:", data.decode())
        except ConnectionResetError:
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))
    
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        message = input("Send: ")
        client_socket.sendall(message.encode())
        if message.lower() == 'exit':
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
