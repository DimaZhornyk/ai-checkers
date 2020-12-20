from functools import reduce

from checkers.board import Board

safe_positions = [1, 2, 3, 4, 5, 12, 13, 20, 21, 28, 29, 30, 31, 32]
player_promotion_line_mapping = {
    1: [29, 39, 31, 32],
    2: [1, 2, 3, 4]
}


def h_peices_num(board: Board, player_num):
    return board.count_movable_player_pieces(player_num) / 12


def h_kings_num(board: Board, player_num):
    cnt = 0
    for piece in board.pieces:
        if piece.player == player_num and piece.king:
            cnt += 1
    return cnt / 12


def h_safe_pieces(board: Board, player_num):
    return reduce(
        lambda count, piece: count + (1 if piece.player == player_num and piece.position in safe_positions else 0),
        board.pieces, 0) / len(safe_positions)


def h_safe_kings(board: Board, player_num):
    return reduce(
        lambda count, piece: count + (
            1 if piece.player == player_num and piece.position in safe_positions and piece.king
            else 0), board.pieces, 0) / len(safe_positions)


def h_num_of_movable_pawns(board: Board, player_num):
    return reduce(
        (lambda count, piece: count + (1 if not piece.captured and piece.is_movable() and piece.player == player_num
                                            and not piece.king else 0)), board.pieces, 0) / 12


def h_num_of_movable_kings(board: Board, player_num):
    return reduce \
               ((lambda count, piece: count + (
                   1 if not piece.captured and piece.is_movable() and piece.player == player_num
                        and piece.king else 0)), board.pieces, 0) / 12


def h_num_of_unoccupied_cells_on_promotion_line(board: Board, player_num):
    return (4 - reduce((lambda count, piece: count + (
        1 if piece.position in player_promotion_line_mapping[player_num] else 0)), board.pieces, 0)) / 4
