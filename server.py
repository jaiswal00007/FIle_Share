import socket
import threading

clients = []

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    clients.append(conn)
    
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            
            # Broadcast the message to all clients except the sender
            for client in clients:
                if client != conn:
                    client.sendall(data)
        
        except ConnectionResetError:
            break

    conn.close()
    clients.remove(conn)
    print(f"Disconnected by {addr}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen()
    print("Server is listening for connections...")
    
    while True:
   #host==conn
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
