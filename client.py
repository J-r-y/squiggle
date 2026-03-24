import socket
import subprocess
import sys
from game import Game


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("localhost", 8080))

        self.game = Game(self.client)


if __name__ == "__main__":
    if "--d" in sys.argv[1:]:
        subprocess.Popen([sys.executable, __file__])
    c = Client()
    sys.exit()
