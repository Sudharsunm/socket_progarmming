import socket

def cel_to_fah(celsius):
    return (celsius * 9/5) + 32

def fah_to_cel(fahrenheit):
    return (fahrenheit - 32) * 5/9

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

print("Server is running and waiting for a connection...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")
    
    data = client_socket.recv(1024).decode()
    
    if data:
        try:
            scale, temp = data.split(":")
            temp = float(temp)
            
            if scale == 'C':
                result = cel_to_fah(temp)
                message = f"{temp}°C is {result:.2f}°F"
            elif scale == 'F':
                result = fah_to_cel(temp)
                message = f"{temp}°F is {result:.2f}°C"
            else:
                message = "Invalid temperature scale! Use 'C' for Celsius and 'F' for Fahrenheit."
        except ValueError:
            message = "Invalid input format. Use 'C:temperature' or 'F:temperature'."
    else:
        message = "No data received."

    client_socket.send(message.encode())
   
    client_socket.close()