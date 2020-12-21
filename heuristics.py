from functools import reduce

from checkers.board import Board
from checkers.piece import Piece

safe_positions = [1, 2, 3, 4, 5, 12, 13, 20, 21, 28, 29, 30, 31, 32]
central_positions = [10, 11, 14, 15, 18, 19, 22, 23]

player_promotion_line_mapping = {
    1: [29, 39, 31, 32],
    2: [1, 2, 3, 4]
}


def h_peices_num(board: Board, player_num):
    return board.count_movable_player_pieces(player_num)


def h_kings_num(board: Board, player_num):
    cnt = 0
    for piece in board.pieces:
        if piece.player == player_num and piece.king:
            cnt += 1
    return cnt


def h_safe_pieces(board: Board, player_num):
    return reduce(
        lambda count, piece: count + (1 if piece.player == player_num and piece.position in safe_positions else 0),
        board.pieces, 0)


def h_safe_kings(board: Board, player_num):
    return reduce(
        lambda count, piece: count + (
            1 if piece.player == player_num and piece.position in safe_positions and piece.king
            else 0), board.pieces, 0)


def h_num_of_movable_pawns(board: Board, player_num):
    return reduce(
        (lambda count, piece: count + (1 if not piece.captured and piece.is_movable() and piece.player == player_num
                                            and not piece.king else 0)), board.pieces, 0)


def h_num_of_movable_kings(board: Board, player_num):
    return reduce \
               ((lambda count, piece: count + (
                   1 if not piece.captured and piece.is_movable() and piece.player == player_num
                        and piece.king else 0)), board.pieces, 0)


def h_num_of_unoccupied_cells_on_promotion_line(board: Board, player_num):
    return (4 - reduce((lambda count, piece: count + (
        1 if piece.position in player_promotion_line_mapping[player_num] else 0)), board.pieces, 0))


def h_num_of_centrally_positioned_pawns(board: Board, player_num):
    return reduce(
        lambda count, piece: count + (
            1 if piece.player == player_num and not piece.captured and piece.position in central_positions else 0),
        board.pieces, 0)


def h_num_of_centrally_positioned_kings(board: Board, player_num):
    return reduce(
        lambda count, piece: count + (
            1 if piece.player == player_num and not piece.captured and piece.position in central_positions and piece.king
            else 0), board.pieces, 0)


bridge = {
    1: [1, 3],
    2: [32, 30]
}

oreo = {
    1: [2, 7, 3],
    2: [30, 26, 31]
}

triangle = {
    1: [1, 6, 2],
    2: [32, 27, 31]
}

dog = {
    1: [1, 5],
    2: [32, 28]
}


def is_piece(piece: Piece, player_num: int):
    return piece is not None and piece.player == player_num


def h_dog_pattern(board: Board, player_num):
    if player_num == 1:
        return is_piece(board.searcher.get_piece_by_position(1), 1) \
               and is_piece(board.searcher.get_piece_by_position(5), 2)
    else:
        return is_piece(board.searcher.get_piece_by_position(32), 2) \
               and is_piece(board.searcher.get_piece_by_position(28), 1)


def h_pattern(board: Board, player_num, pattern):
    for pos in pattern[player_num]:
        if not is_piece(board.searcher.get_piece_by_position(pos), player_num):
            return -1
    return 1


def h_triangle_pattern(board: Board, player_num):
    return h_pattern(board, player_num, triangle)


def h_oreo_pattern(board: Board, player_num):
    return h_pattern(board, player_num, oreo)


def h_bridge_pattern(board: Board, player_num):
    return h_pattern(board, player_num, bridge)
