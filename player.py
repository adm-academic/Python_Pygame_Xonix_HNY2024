import pygame
import random
import os
import inspect
import sys

class Player():
    def __init__(self, game, settings):  # констуктор
        self.game = game
        self.settings = settings
        self.score = 0
