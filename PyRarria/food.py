import pygame
from settings import *
from Items import *

class Food(Item):
    def __init__(self, x, y, name, game):
        super().__init__(x, y, name, game)

    def akcja(self):
        pass