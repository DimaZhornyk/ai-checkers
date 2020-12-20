import copy
import math
import random
from datetime import datetime
import time
import multiprocessing as mp
from checkers.game import Game

from node import Node


class Minimax:

    def __init__(self, player_num):
        self.turn_limit = 100
        self.turn_count = 0
        self.player_num = player_num
        self._evaluation_start = None
        self._move_time = 4

    def best_move(self, game: Game, player_num: int):
        self._evaluation_start = datetime.now()
        root = Node(game, player_num, None)
        q = mp.Queue()
        q.put(root)
        cpu_count = int(mp.cpu_count() - 1)
        pool = mp.Pool(cpu_count, self.mp_child_creation, (q,))
        time.sleep(self._move_time)
        pool.terminate()
        move = self.find_best_move(root)
        return move

    def mp_child_creation(self, queue):
        while True:
            node = queue.get()
            queue.put(random.randint(0, 1000))
            for move in node.board.get_possible_moves():
                c_game = copy.deepcopy(node.board)
                c_game.move(move)
                new_node = Node(c_game, self.player_num, move)
                node.add_children(new_node)
                if c_game.is_over():
                    continue
                queue.put(new_node)

    def find_best_move(self, node: Node):
        best_val = self.minimax(node, 0, True, float('-inf'), float('inf'))
        # TODO extract move which leads to child node
        for c in node.children:
            if c.weight == best_val:
                return c.move

    def minimax(self, node, depth, isMaximizingPlayer, alpha, beta):
        if len(node.children) == 0:
            return node.evaluate(node.count_heuristics())
        
        if isMaximizingPlayer:
            best_val = float('-inf')
            for child in node.children:
                value = self.minimax(child, depth + 1, False, alpha, beta)
                best_val = max(best_val, value)
                node.weight = best_val
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break
            return best_val

        else:
            best_val = float('inf')
            for child in node.children:
                value = self.minimax(child, depth + 1, True, alpha, beta)
                best_val = min(best_val, value)
                node.weight = best_val
                beta = min(beta, best_val)
                if beta <= alpha:
                    break
            return best_val

