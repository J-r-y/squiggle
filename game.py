import json
from socket import socket
import threading
import zlib
import pygame as pg

from ui.menu import Menu
from ui.canvas import Canvas
from ui.palette import Palette
from ui.chat import Chat
from ui.textfield import Textfield
from util.flexbox import Flexbox
from util.style import Style


class Game:
    def __init__(self, client: socket):
        if not pg.init():
            return

        self.client = client

        self.screen = pg.display.set_mode((1280, 720))
        self.font = pg.font.Font("Poppins.ttf", 20)

        self.menu = Menu()
        self.palette = Palette(Style(height=0.1))
        self.canvas = Canvas(self.palette, self.send_bytes)
        self.chat = Chat(self.font)
        self.textfield = Textfield(self.send_message, self.font, Style(height=0.1))

        self.pre_view = Flexbox(
            (Textfield(self.send_message, self.font, Style(width=200, height=100)),),
            (100, 100, 200, 200),
        )
        self.pre_view.set_sizes(self.pre_view.get_space())
        self.pre_view.set_positions()
        self.game_view = Flexbox(
            (
                self.menu,
                Flexbox(
                    (self.canvas, self.palette),
                    style=Style(width=0.6, direction="col"),
                ),
                Flexbox((self.chat, self.textfield), style=Style(direction="col")),
            ),
            (140, 110, 1000, 500),
        )

        self.game_view.set_sizes(self.game_view.get_space())
        self.game_view.set_positions()

        self.name: str = ""

        pg.key.set_repeat(200, 50)
        self.keys = set()

        self.clock = pg.time.Clock()
        self.running = True
        self.run()

    def run(self):
        threading.Thread(target=self.handle_conn, daemon=True).start()
        while self.running:
            self.update()
            self.render()
            self.clock.tick(60)

    def update(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

            self.pre_view.update(e)

    def render(self):
        self.screen.fill(pg.Color("cyan"))
        self.pre_view.draw(self.screen)

        pg.display.update()

    def handle_conn(self):
        try:
            while header := self.client.recv(4):
                data_len = int.from_bytes(header, "big")
                payload = self.client.recv(data_len)
                data = json.loads(zlib.decompress(payload))
                match data["type"]:
                    case "msg":
                        self.chat.add_message(data["name"], data["msg"])
                    case "canvas":
                        self.canvas.draw_circle(*data["event"])

        except Exception as e:
            print(f"Error in client: {e}")
        finally:
            self.client.close()
            print("Connection to server closed")

    def send_message(self, message: str):
        data = json.dumps({"type": "msg", "name": self.name, "msg": message}).encode()
        self.chat.add_message(self.name, message)
        self.send_bytes(data)

    def send_bytes(self, data: bytes):
        compressed = zlib.compress(data)
        self.client.send(len(compressed).to_bytes(4, "big") + compressed)
