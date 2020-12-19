import math

from checkers.board import Board

from game import Game
import copy

turn_limit = 100

turn_count = 0


def make_best_move(maximizer_mark: int, board: Board) -> []:
    best_score = -math.inf
    best_move = None
    for move in board.get_possible_moves():
        new_board = board.create_new_board_from_move(move)
        score = minimax(True, maximizer_mark, new_board)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def minimax(maximizing: bool, maximizer_mark: int, board: Board) -> []:
    # if time is over calc
    global turn_count
    global turn_limit
    moves = board.get_possible_moves()
    if not moves or turn_count > turn_limit:
        winner = get_winner(board)
        heur = abs(board.count_movable_player_pieces(1) - board.count_movable_player_pieces(2))
        return heur if winner == maximizer_mark else - heur # return score here
    scores = []
    turn_count += 1
    for move in moves:
        new_board = board.create_new_board_from_move(move)
        scores.append(minimax(not maximizing, maximizer_mark, new_board))

    return max(scores) if maximizing else min(scores)


def heuristic(board: Board) -> []:
    pass


def get_winner(board: Board):
    # compare heuristic scores to choose winner
    if board.count_movable_player_pieces(1) < board.count_movable_player_pieces(2):
        return 2
    else:
        return 1

