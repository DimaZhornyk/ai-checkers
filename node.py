from checkers.game import Game
from multiprocessing import Queue, Manager
from heuristics import *


class Node:
    def __init__(self, game: Game, move):
        self.game = game
        self.move = move
        self.board = game.board
        self.weight = 0
        self.children = list()

    def add_children(self, children):
        self.children.append(children)
