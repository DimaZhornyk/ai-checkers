import copy
import random
from datetime import datetime
import time
import multiprocessing as mp
from checkers.game import Game

from heuristics import *


class Node:
    def __init__(self, game: Game, player_num, move):
        self.move = move
        self._board = game.board
        self._player_num = player_num
        self.weight = 0
        self.children = []

    def evaluate(self, heuristics):
        res = sum(heuristics) / len(heuristics)
        self.weight = res
        return res

    def add_children(self, children):
        self.children.append(children)

    def count_heuristics(self):
        heurs = [h_peices_num(self._board, self._player_num),
                 h_kings_num(self._board, self._player_num),
                 h_safe_pieces(self._board, self._player_num),
                 h_safe_kings(self._board, self._player_num),
                 h_num_of_movable_pawns(self._board, self._player_num),
                 h_num_of_movable_kings(self._board, self._player_num)]
        print(
            f"Num pieces: {heurs[0]}, kings num: {heurs[1]}, safe pieces: {heurs[2]}, safe kings: {heurs[3]},"
            f" num of mov pawns: {heurs[4]}, num of movable kings: {heurs[5]}")
        return heurs
