import socket
import threading

def receive(con):
    while 1:
        data=con.recv(1024)
        if not data:
            break
        print(f"Received: {data.decode()}\nSend: ", end='', flush=True)


def start_client():
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(('192.168.0.157',65432))
    threading.Thread(target=receive,args=(client,)).start()
    while True:
        message=input("Send:")
        client.sendall(message.encode())
        if(message.lower=="exit"):
            break
    client.close()

start_client()