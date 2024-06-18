def send(socket, message):
    sent_data = message.encode(encoding='utf-8', errors='ignore')

    socket.send(sent_data)

def recv(socket, size):
    incoming_data = socket.recv(size)

    return incoming_data.decode(encoding='utf-8', errors='ignore')