import socket
import threading
import tkinter as tk
from tkinter import filedialog
import random
import os

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
        server_socket.bind(('localhost', 65432))
        server_socket.listen()
        print("Server started, waiting for connections...")

        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    except Exception as e:
        print(f"Error: {e}")
        return -1

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))
    return client_socket

def show_overlay(sock):
    overlay = tk.Frame(root, bg="grey")
    overlay.place(x=0, y=0, relwidth=1, relheight=1)
    # Chat display
    chat_display = tk.Text(overlay, width=70, height=20, wrap=tk.WORD, bg="black", fg="white", font=("Arial", 12), state=tk.DISABLED)
    chat_display.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    # function to display received messages
    def receive_messages(sock):
        while True:
            try:
                data = sock.recv(1024)
                if not data:
                    break
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, f"Received: {data.decode()}\n")  # Display received message
                chat_display.config(state=tk.DISABLED)
                chat_display.yview(tk.END)
            except ConnectionResetError:
                break

    # used seperate thread for receiving messages
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    # Frame to take user input
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
            chat_display.insert(tk.END, f"You: {message}\n")  # Display 
            chat_display.config(state=tk.DISABLED)
            chat_display.yview(tk.END)
            user_input.delete(0, tk.END)

    def send_file():
        if file_path:
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)

            # Notify the server about the file
            sock.sendall(f"FILE {file_size} {file_name}".encode())  # used to notify server about file size & name

            # Send the file content in chunks
            with open(file_path, "rb") as file:
                while chunk := file.read(1024):
                    sock.sendall(chunk)  # Send each chunk

            # Display file sent in the chat window
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"You: File sent: {file_name}\n")  # Display file send message
            chat_display.config(state=tk.DISABLED)
            chat_display.yview(tk.END)

    send_button = tk.Button(input_frame, text="Send", command=send_message, bg="white", fg="black", font=("Arial", 12,"bold"))
    send_button.pack(side=tk.RIGHT, padx=10, pady=10)

    file_button = tk.Button(input_frame, text="Upload File", command=select_file, bg="white", fg="black", font=("Arial", 12,"bold"))
    file_button.pack(side=tk.RIGHT, padx=10, pady=10)

    send_file_button = tk.Button(input_frame, text="Send File", command=send_file, bg="white", fg="black", font=("Arial", 12,"bold"))
    send_file_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Close button
    close_button = tk.Button(overlay, text="✖", command=overlay.destroy, bg="red", fg="red", font=("Arial", 15))
    close_button.place(x=840, y=10)

def create_room(event=None):
    def run_server():
        start_server()

    # Start the server in a new thread
    threading.Thread(target=run_server, daemon=True).start()

    # Connect client to the newly created server
    sock = start_client()
    show_overlay(sock)

def join_room(event=None):
    sock = start_client()
    show_overlay(sock)

#  Application UI -------->


root = tk.Tk()
root.title("GetChat")
root.geometry("900x600")
root.configure(bg="black")

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

# start animation
animate()  
root.mainloop()
