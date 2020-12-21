import copy
import random

from game import Game
from heuristics import *
from node import Node


class Minimax:

    def __init__(self, player_number):
        self.player_num = player_number

    def best_move(self, game: Game, depth):
        root = Node(game, None)
        res = self.minimax(root, depth, float('-inf'), float('inf'))
        for node in root.children:
            if node.weight == res:
                return node.move
        return random.choice(game.get_possible_moves())

    def minimax(self, node: Node, depth, alpha, beta):
        if depth == 0 or node.game.is_over():
            node.weight = self.evaluate(self.count_heuristics(node.game))
            return node.weight

        if node.game.whose_turn() == self.player_num:
            value = float('-inf')
            for move in node.game.get_possible_moves():
                new_game = copy.deepcopy(node.game)
                new_game.move(move)
                new_node = Node(new_game, move)
                node.add_children(new_node)
                value = max(self.minimax(new_node, depth - 1, alpha, beta), value)
                node.weight = value
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float('inf')
            for move in node.game.get_possible_moves():
                new_game = copy.deepcopy(node.game)
                new_game.move(move)
                new_node = Node(new_game, move)
                node.add_children(new_node)
                value = min(self.minimax(new_node, depth - 1, alpha, beta), value)
                node.weight = value
                alpha = min(alpha, value)
                if alpha <= beta:
                    break
            return value

    def evaluate(self, heuristics):
        res = 0
        coefficients = [10, 7, 2, 2, -30, -30, 100, 100, 100, 100]
        # coefficients = [5, 6, -3, -3, 5, 5, 5, 5]
        for i in range(len(heuristics)):
            res += heuristics[i] * coefficients[i]
        # print("RESULT: ", res)
        return res

    def count_heuristics(self, game):
        board = game.board
        player_num = game.whose_turn()
        enemy_num = 1 if player_num == 2 else 2
        # Number of pawns
        heurs = [h_peices_num(board, player_num) - h_peices_num(board, enemy_num),  # Number of pawns
                 h_kings_num(board, player_num) - h_kings_num(board, enemy_num),  # Number of kings

                 h_safe_pieces(board, player_num),
                 # Number of attacking pawns (i.e. positioned in three topmost rows)
                 h_safe_kings(board, player_num),  #

                 h_num_of_centrally_positioned_pawns(board, player_num),

                 h_num_of_centrally_positioned_kings(board, player_num),

                 h_bridge_pattern(board, player_num),
                 h_oreo_pattern(board, player_num),
                 h_triangle_pattern(board, player_num),
                 h_dog_pattern(board, player_num)
                 ]
        print(heurs)
        return heurs
