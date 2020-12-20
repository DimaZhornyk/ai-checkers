import copy
import multiprocessing as mp
import random

from heuristics import *


class Minimax:

    def mp_new_move(self, game, depth, move, maximizing_player):
        alpha = float("-inf")
        new_game = copy.deepcopy(game)
        new_game.move(move)
        best_move = None
        beta = self.minimax(new_game, depth, maximizing_player, float('-inf'), float('inf'))
        if beta > alpha:
            alpha = beta
            best_move = move
        return alpha, best_move

    def best_move(self, game, depth):
        cpu_count = int(mp.cpu_count() - 1)
        with mp.Pool(processes=cpu_count) as pool:
            res = pool.starmap(self.mp_new_move, [(game, depth - 1, move, True) for move in game.get_possible_moves()])
        m_val = [0, random.choice(game.get_possible_moves())]
        for item in res:
            if item[0] > m_val[0]:
                m_val = item
        return m_val[1]

    def minimax(self, game, depth, isMaximizingPlayer, alpha, beta):
        if depth == 0 or game.is_over():
            return self.evaluate(self.count_heuristics(game))

        if isMaximizingPlayer:
            value = float('-inf')
            for move in game.get_possible_moves():
                new_game = copy.deepcopy(game)
                new_game.move(move)
                value = max(self.minimax(new_game, depth - 1, False, alpha, beta), value)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float('inf')
            for move in game.get_possible_moves():
                new_game = copy.deepcopy(game)
                new_game.move(move)
                value = min(self.minimax(new_game, depth - 1, False, alpha, beta), value)
                alpha = min(alpha, value)
                if beta <= alpha:
                    break
            return value

    def evaluate(self, heuristics):
        res = 0
        coefficients = [5, 7, 2, 2, 1, 1]
        for i in range(len(heuristics)):
            res += heuristics[i] * coefficients[i]
        # res = sum(heuristics) / len(heuristics)
        return res

    def count_heuristics(self, game):
        board = game.board
        player_num = game.whose_turn()
        # Number of pawns
        heurs = [h_peices_num(board, player_num),  # Number of pawns
                 h_kings_num(board, player_num),  # Number of kings
                 h_safe_pieces(board, player_num),  # Number of attacking pawns (i.e. positioned in three topmost rows)
                 h_safe_kings(board, player_num),  #
                 h_num_of_movable_pawns(board, player_num),
                 h_num_of_movable_kings(board, player_num)]
        return heurs
