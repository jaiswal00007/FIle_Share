import socket
import threading
#defining the connection
clients=[]
def handle_client(con,addr):
    print(f"Connected by {addr}")
    clients.append(con)
    while 1:
        data=con.recv(1024)
        if not data:
            break
        for client in clients:
            if(client!=con):
                client.sendall(data)
    con.close()
    
    clients.remove(con)
    print(f"Disconnected By {addr}")




def start_server():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('localhost',9099))
    server.listen()
    print("Server is Listening....")

    while 1:
        con,addr=server.accept()
        t=threading.Thread(target=handle_client,args=(con,addr))
        t.start()

start_server()
    # print(f"Connected with {addr}")
    # r=con.recv(1024).decode('utf-8')
    # print(r,"\n")


