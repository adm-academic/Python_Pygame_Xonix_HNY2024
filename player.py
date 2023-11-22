import pygame
import random
import os
import inspect
import sys

class Player():
    def __init__(self, yy, xx, game, settings):  # констуктор
        self.game = game
        self.settings = settings
