from socket import socket
import pygame as pg

from ui.canvas import Canvas
from ui.chat import Chat
from ui.textfield import Textfield
from util.group import Group


class Game:
    def __init__(self, client: socket):
        init = pg.init()
        if not init:
            return

        self.client = client

        self.screen = pg.display.set_mode((1280, 720))
        self.font = pg.font.Font("Poppins.ttf", 20)
        self.sprites = Group()

        self.sprites.add(
            Canvas(275, 100, 700, 540),
            Chat(self.font, 1000, 100, 200, 490),
            Textfield(self.handle_send, self.font, 1000, 600),
        )

        pg.key.set_repeat(200, 50)
        self.keys = set()

        self.clock = pg.time.Clock()
        self.running = True
        self.run()

    def run(self):
        while self.running:
            self.update()
            self.render()
            self.clock.tick(60)

    def update(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

            self.sprites.update(e)

    def render(self):
        self.screen.fill(pg.Color("cyan"))
        self.sprites.draw(self.screen)

        pg.display.update()

    def handle_send(self, message: str):
        self.client.send(message.encode())
