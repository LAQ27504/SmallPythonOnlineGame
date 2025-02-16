import socket

# filepath: /home/laq275/LAQ/Classes/SmallPythonOnlineGame/client/client.py

def main():
    host = '192.168.1.8'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    can_send = True
    while True:
        message = client_socket.recv(1024).decode()
        if not message:
            break
        print(message)
        if message == 'You are dead. You will spectate the game':
            can_send = False
        if can_send:
            response = input("> ")
        client_socket.sendall(response.encode())

    client_socket.close()

if __name__ == "__main__":
    main()