import socket

class ClientTaches:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        self.sock = socket.create_connection((host, port))

    def envoyer(self, msg):
        self.sock.sendall(msg.encode())
        return self.sock.recv(4096).decode()

    def close(self):
        self.sock.close()
