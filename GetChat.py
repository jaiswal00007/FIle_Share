import socket
import threading
import tkinter as tk
from tkinter import filedialog
import random
import os
import ipaddress

clients = []

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    clients.append(conn)

    # notify all clients when someone connects
    for client in clients:
        if client != conn:
            client.sendall(f"Connected by {addr}\n".encode())

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            # condition if it's a file message 
            if data.startswith(b"FILE"):
                # handle receiving file
                f_size = int(data.split()[1])
                f_name = data.split()[2].decode()
                with open(f"received_{f_name}", "wb") as f:
                    remaining_size = f_size
                    while remaining_size > 0:
                        file_data = conn.recv(min(remaining_size, 1024))
                        f.write(file_data)
                        remaining_size -= len(file_data)

                # to inform all clients about the received file
                for client in clients:
                    if client != conn:
                        client.sendall(f"Received file: {f_name}\n".encode())
            else:
                # used to broadcast txt message
                for client in clients:
                    if client != conn:
                        client.sendall(data)

        except ConnectionResetError:
            break

    conn.close()
    clients.remove(conn)
    print(f"Disconnected by {addr}")
    
    # send all about disconnects client info 
    for client in clients:
        client.sendall(f"Disconnected by {addr}\n".encode())

def start_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 65432))
        server_socket.listen()
        print("Server started, waiting for connections...")

        while True:
            try:
                conn, addr = server_socket.accept()
                threading.Thread(target=handle_client, args=(conn, addr)).start()
            except KeyboardInterrupt:
                print("Server shutting down...")
                for client in clients:
                    client.sendall("Server is shutting down.\n".encode())
                    client.close()
                server_socket.close()
                break
    except Exception as e:
        print(f"Error: {e}")
        return -1


def start_client():
    k=ip.get().strip()
    if(k=="Enter IP Address..." or not k):
        k='127.0.0.1'
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # client_socket.settimeout(5)  # timeout of 5 seconds
        client_socket.connect((k, 65432))
    except (socket.timeout, ConnectionRefusedError) as e:
        return -1
    except socket.gaierror as e:
        return -1
    except Exception as e:
        return -1
    return client_socket
def safe_update_chat_display(chat_display, message):
    if chat_display.winfo_exists():  # chk widget exists
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, message)
        chat_display.config(state=tk.DISABLED)
        chat_display.yview(tk.END)

def show_overlay(sock):
    overlay = tk.Frame(root, bg="grey")
    overlay.place(x=0, y=0, relwidth=1, relheight=1)
    # display-Chat
    chat_display = tk.Text(overlay, width=70, height=20, wrap=tk.WORD, bg="black", fg="white", font=("Arial", 12), state=tk.DISABLED)
    chat_display.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    # display received messages
    def receive_messages(sock):
        try:
            while True:
                data = sock.recv(1024)
                if not data:
                    raise ConnectionResetError("No data received. Disconnecting.")
                message = f"Received: {data.decode()}\n"
                root.after(0, safe_update_chat_display, chat_display, message)
        except (ConnectionResetError, OSError):
            root.after(0, safe_update_chat_display, chat_display, "Disconnected from server.\n")
        finally:
            root.after(0, overlay.destroy)
            sock.close()
            print("Client disconnected.")




    # used seperate thread for receiving messages
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    # to take user input
    input_frame = tk.Frame(overlay, bg="grey")
    input_frame.pack(side=tk.BOTTOM, fill=tk.X)

    user_input = tk.Entry(input_frame, width=80, font=("Arial", 12), bg="black", fg="white", insertbackground="white")
    user_input.pack(side=tk.LEFT, padx=10, pady=10)
    # user_input.bind("<Return>", send_message) for binding enter key with send button

    file_path = None  

    def select_file():
        nonlocal file_path
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("All Files", "*.*")])

    def send_message():
        message = user_input.get()
        if message:
            sock.sendall(message.encode())  # used for Sending message to server
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"You: {message}\n")  # display 
            chat_display.config(state=tk.DISABLED)
            chat_display.yview(tk.END)
            user_input.delete(0, tk.END)

    def send_file():
        if file_path:
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)

            # notify the server about the file
            sock.sendall(f"FILE {file_size} {file_name}".encode())  # used to notify server about file info
            # Send in chunks
            with open(file_path, "rb") as file:
                while chunk := file.read(1024):
                    sock.sendall(chunk)  # each chunk one by one

            # to display file sent
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"You: File sent: {file_name}\n")  # file send message 
            chat_display.config(state=tk.DISABLED)
            chat_display.yview(tk.END)

    # to close client upon exiting 'X'
    def close_client(sock, overlay):
        try:
            sock.close()
        except:
            pass
        if overlay.winfo_exists():
            overlay.destroy()
        print("Client disconnected.")


    send_button = tk.Button(input_frame, text="Send", command=send_message, bg="white", fg="black", font=("Arial", 12,"bold"))
    send_button.pack(side=tk.RIGHT, padx=10, pady=10)

    file_button = tk.Button(input_frame, text="Upload File", command=select_file, bg="white", fg="black", font=("Arial", 12,"bold"))
    file_button.pack(side=tk.RIGHT, padx=10, pady=10)

    send_file_button = tk.Button(input_frame, text="Send File", command=send_file, bg="white", fg="black", font=("Arial", 12,"bold"))
    send_file_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # close button
    close_button = tk.Button(overlay, text="✖", command=lambda: close_client(sock, overlay), bg="red", fg="red", font=("Arial", 15))

    close_button.place(relx=0.99,rely=0.02, anchor="ne")

def create_room(event=None):
    def run_server():
        start_server()

    # new thread
    threading.Thread(target=run_server, daemon=True).start()

    # cleint connects
    sock = start_client()
    show_overlay(sock)
def show_warn(chk):
    overlay = tk.Frame(root, bg="grey")
    overlay.place(x=200, y=150, relwidth=0.5, relheight=0.5)
    txt=tk.Label(text=chk,font=("Arial",18,"bold"),bg="grey",fg="red")

    txt.place(x=320,y=280)
    def close():
        txt.destroy()
        overlay.destroy()


    close_button = tk.Button(overlay, text="✖", command=close, bg="red", fg="red", font=("Arial", 15))
    close_button.place(x=400, y=0)


# to check ip is valid or not return bool
def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def join_room(event=None):
    if(ip.get()=="Enter IP Address..." or not ip.get()):
        show_warn("First Enter IP Address...")
    else:
        if(is_valid_ip(ip.get())):
            sock = start_client()
            if(sock!=-1):
                show_overlay(sock)
        else:
            show_warn("Enter Valid IP Address...")

#  Application UI -------->


root = tk.Tk()
root.title("GetChat")
root.geometry("900x600")
root.configure(bg="black")
root.minsize(width=900,height=600)
# root.maxsize(width=900,height=600)
global ip
ip=tk.StringVar()
# widget
canvas = tk.Canvas(root, width=900, height=600, bg="black")
canvas.pack()

colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"]
circles = []
speeds = []

# for moving or animating circles
for _ in range(20):
    x0, y0 = random.randint(0, 750), random.randint(0, 550)
    color = random.choice(colors)
    circle = canvas.create_oval(x0, y0, x0 + 20, y0 + 20, fill=color, outline="")
    circles.append(circle)
    speeds.append((random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])))

def animate():
    for i, circle in enumerate(circles):
        dx, dy = speeds[i]
        canvas.move(circle, dx, dy)
        x1, y1, x2, y2 = canvas.coords(circle)

        # wall bounce
        if x1 <= 0 or x2 >= 900:
            speeds[i] = (-dx, dy)
        if y1 <= 0 or y2 >= 600:
            speeds[i] = (dx, -dy)

    # after 30s the next animation frame
    root.after(30, animate)

# buttons to create or join room
button_rect1 = canvas.create_rectangle(280, 220, 415, 280, fill="", outline="white", width=2)
button_text1 = canvas.create_text(350, 250, text="Create Room", fill="white", font=("Arial", 16))

button_rect2 = canvas.create_rectangle(480, 220, 615, 280, fill="", outline="white", width=2)
button_text2 = canvas.create_text(550, 250, text="Join Room", fill="white", font=("Arial", 16))

# click binding with method
canvas.tag_bind(button_rect1, "<Button-1>", create_room)
canvas.tag_bind(button_text1, "<Button-1>", create_room)

canvas.tag_bind(button_rect2, "<Button-1>", join_room)
canvas.tag_bind(button_text2, "<Button-1>", join_room)
entry = tk.Entry(root, width=18 , font=("Arial", 18), bg="black", fg="white", insertbackground="white",highlightbackground="white",textvariable=ip)
def on_focus_in(event):
    if entry.get() == "Enter IP Address...":  # txt for placeholder
        entry.delete(0, tk.END)


# set placeholder text
entry.insert(0, "Enter IP Address...")

# <focusin> used when user type
entry.bind("<FocusIn>", on_focus_in)
entry.place(relx=0.5, rely=0.65, anchor="center")  
# entry.place(x=340, y=400) 
# start animation
animate()  
root.mainloop()