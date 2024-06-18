import socket
import socketFuncs

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = '127.0.0.1'
server_port = 8080
server_address = (server_ip, server_port)

sock.connect(server_address)

try:
    while True:
        socketFuncs.send(sock, input('Введите сообщение: '))

        incoming_data = socketFuncs.recv(sock, 1024)

        if incoming_data == 'shut_down':
            socketFuncs.send(sock, 'shut_down')

            break

        else:
            print(f'Сервер: {incoming_data}')

finally:
    print(f'Соединение с {server_address} закрыто')

    sock.close()