import socket


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("localhost", 8080))
        self.server.listen(5)

        self.listen()

    def listen(self):
        while True:
            conn, addr = self.server.accept()

            print(conn.recv(1024).decode())


if __name__ == "__main__":
    s = Server()
