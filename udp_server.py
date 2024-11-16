import socket

def cel_to_fah(celsius):
    return (celsius * 9/5) + 32


def fah_to_cel(fahrenheit):
    return (fahrenheit - 32) * 5/9

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 12345))

print("UDP server is running and waiting for data...")

while True:
    data, client_address = server_socket.recvfrom(1024)
    data = data.decode()

    if data:
        try:
            scale,temp = data.split(":")
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

    server_socket.sendto(message.encode(), client_address)