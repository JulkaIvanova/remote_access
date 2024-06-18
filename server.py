import socket
import socketFuncs
import webbrowser
import subprocess
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = 'localhost' # 127.0.0.1
# host_name = socket.gethostname()
# host = socket.gethostbyname_ex(host_name)
# ip = host[-1][-1]
port = 8080
server_address = (ip, port)

sock.bind(server_address)
sock.listen(1)

while True:
    print('Ожидание подключения...')

    connection, client_address = sock.accept()

    try:
        print(f'Подключено к {client_address}')

        while True:
            incoming_data = socketFuncs.recv(connection, 1024)

            if incoming_data == 'shut_down':
                socketFuncs.send(connection, 'shut_down')

                break

            elif incoming_data == 'open_url':
                socketFuncs.send(connection, 'Отправьте url')

                url = socketFuncs.recv(connection, 1024)

                webbrowser.open(url)

                socketFuncs.send(connection, 'Операция выполнена!')

            elif incoming_data == "make_dir":
                socketFuncs.send(connection, 'Отправьте полный путь до места создания папки')
                path = socketFuncs.recv(connection, 4096)
                socketFuncs.send(connection, 'Отправьте название папки')
                name = socketFuncs.recv(connection, 1024)
                cmd = f"cd {path} & mkdir {name}"
                if os.system(cmd) == 0:
                    socketFuncs.send(connection, 'Папка создана')
                else:
                    socketFuncs.send(connection, "Ошибка")


            elif incoming_data == "SHUT_DOWN":
                socketFuncs.send(connection, 'Отправьте количество секунд через которое выключить компьютер')
                seconds = socketFuncs.recv(connection, 1024)
                try:
                    a = os.system(f"shutdown /s /t {seconds}")
                finally:
                    if a == 1:
                        socketFuncs.send(connection, "Ошибка")
                    else:
                        socketFuncs.send(connection, "shut_down")
            # Из-за проблем с кодировкой функция работает некорекктно
            elif incoming_data == "show_wi-fi_key":
                socketFuncs.send(connection, 'Отправьте название сети')
                name = socketFuncs.recv(connection, 1024)
                try:
                    socketFuncs.send(connection, subprocess.check_output(f'netsh wlan show profile name="{name}" key=clear', bufsize=1024, shell=True).decode(encoding='utf-8', errors='ignore'))
                except Exception as err:
                    print(err)
                    socketFuncs.send(connection, "Ошибка")
                os.system(f'netsh wlan show profile name="{name}" key=clear > 123.txt')
                os.system("notepad++ 123.txt")
            elif incoming_data == 'write':
                socketFuncs.send(connection, 'напишите текст')
                text = socketFuncs.recv(connection, 1024)
                socketFuncs.send(connection, 'перезаписать файл (>) или добавить в файл (>>)')
                b = socketFuncs.recv(connection, 1024)
                if b != ">" or b != ">>":
                    while True:
                        if b == ">" or b == ">>":
                            break
                        print(type(b))
                        socketFuncs.send(connection, 'Напишите > (Перезаписать) или >> (Добавить)')
                        b = socketFuncs.recv(connection, 1024)
                socketFuncs.send(connection, 'Введите имя текстого файла')
                name = socketFuncs.recv(connection, 1024)
                socketFuncs.send(connection, 'Введите путь до файла')
                path = socketFuncs.recv(connection, 1024)
                cmd = f"cd {path} & echo {text} {b} {name}.txt"
                cmd2 = f"cd {path} & notepad++ {name}.txt"
                if os.system(cmd) == 0 and os.system(cmd2) == 0:
                    socketFuncs.send(connection, 'Успех')
                else:
                    socketFuncs.send(connection, 'Ошибка')
            elif incoming_data == 'copy':
                socketFuncs.send(connection, 'Введите путь до копируемого файла')
                path = socketFuncs.recv(connection, 1024)
                socketFuncs.send(connection, 'Введите путь до места копирования')
                path2 = socketFuncs.recv(connection, 1024)
                if os.system(f"copy {path} {path2}") == 0:
                    socketFuncs.send(connection, 'Файлы скопированы')
                else:
                    socketFuncs.send(connection, 'ошибка')


                



            else:
                print(f'Клиент: {incoming_data}')

                socketFuncs.send(connection, input('Введите сообщение: '))

    finally:
        print(f'Соединение с {client_address} закрыто')

        connection.close()
