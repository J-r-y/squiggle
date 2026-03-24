import socket
import sys
import threading


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("localhost", 8080))
        self.server.listen(5)
        self.clients = set()

        self.listen()

    def listen(self):
        try:
            while True:
                conn, addr = self.server.accept()
                thread = threading.Thread(
                    target=self.handle_conn, args=(conn,), daemon=True
                )
                thread.start()
                self.clients.add(conn)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.server.close()
            sys.exit(1)

    def broadcast(self, data: bytes, conn: socket.socket):
        for client in self.clients:
            if conn is not client:
                client.send(data)

    def handle_conn(self, conn: socket.socket):
        try:
            while msg := conn.recv(1024):
                self.broadcast(msg, conn)

        except Exception as e:
            print(f"Erorr: {e}")
        finally:
            print(
                f"Closed connection: {':'.join(map(lambda x: str(x), conn.getsockname()))}"
            )
            self.clients.remove(conn)
            conn.close()


if __name__ == "__main__":
    s = Server()
