import socket
import tkinter as tk
from tkinter import messagebox

def validate_scale():
    scale = scale_var.get().upper()
    
    # Check if scale is valid ('C' or 'F')
    if scale in ('C', 'F'):
        temp_entry.grid(row=2, column=1)  # Show the temperature field
        send_button.grid(row=3, column=1)  # Show the send button
    else:
        temp_entry.grid_forget()  # Hide the temperature field
        send_button.grid_forget()  # Hide the send button
        messagebox.showerror("Input Error", "Scale must be 'C' for Celsius or 'F' for Fahrenheit.")

def send_message():
    scale = scale_var.get().upper()
    temp = temp_var.get()
    method = method_var.get()

    # Validate the scale input again
    if scale not in ('C', 'F'):
        messagebox.showerror("Input Error", "Scale must be 'C' for Celsius or 'F' for Fahrenheit.")
        return

    # Validate temperature input
    if not temp:
        messagebox.showerror("Input Error", "Temperature must be provided.")
        return

    try:
        float(temp)  # Check if temp is a valid number
    except ValueError:
        messagebox.showerror("Input Error", "Temperature must be a valid number.")
        return

    message = f"{scale}:{temp}"

    if method == "UDP":
        send_udp_message(message)
    elif method == "TCP":
        send_tcp_message(message)

def send_udp_message(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)
    
    client_socket.sendto(message.encode(), server_address)
    response, _ = client_socket.recvfrom(1024)
    messagebox.showinfo("Server Response", response.decode())
    
    client_socket.close()

def send_tcp_message(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    
    client_socket.send(message.encode())
    response = client_socket.recv(1024).decode()
    messagebox.showinfo("Server Response", response)

    client_socket.close()

# GUI setup
root = tk.Tk()
root.title("TCP/UDP Temperature Conversion")

# Method selection (TCP/UDP)
tk.Label(root, text="Select Method:").grid(row=0, column=0)
method_var = tk.StringVar(value="UDP")
tk.Radiobutton(root, text="UDP", variable=method_var, value="UDP").grid(row=0, column=1)
tk.Radiobutton(root, text="TCP", variable=method_var, value="TCP").grid(row=0, column=2)

# Temperature scale input
tk.Label(root, text="Temperature Scale (C/F):").grid(row=1, column=0)
scale_var = tk.StringVar()
scale_entry = tk.Entry(root, textvariable=scale_var)
scale_entry.grid(row=1, column=1)

# Add a button to validate scale and show temperature field
validate_button = tk.Button(root, text="Enter Scale", command=validate_scale)
validate_button.grid(row=1, column=2)

# Temperature value input (initially hidden)
tk.Label(root, text="Temperature:").grid(row=2, column=0)
temp_var = tk.StringVar()
temp_entry = tk.Entry(root, textvariable=temp_var)
temp_entry.grid_forget()  # Initially hidden

# Send button (initially hidden)
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid_forget()  # Initially hidden

root.mainloop()
