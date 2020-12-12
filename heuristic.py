# from math import log, sqrt
# from random import choice
#
#
# class MonteCarlo(object):
#
#     def __init__(self, board, **kwargs):
#         self.max_moves = None
#         self.board = board
#         self.wins = 0
#         self.plays = 0
#         self.states = 0
#         self.C = kwargs.get('C', 1.4)
#
#
#     def run_simulation(self):
#         # A bit of an optimization here, so we have a local
#         # variable lookup instead of an attribute access each loop.
#         plays, wins = self.plays, self.wins
#
#         visited_states = set()
#         states_copy = self.states[:]
#         state = states_copy[-1]
#         player = self.board.current_player(state)
#
#         expand = True
#         for t in range(1, self.max_moves + 1):
#             legal = self.board.legal_plays(states_copy)
#             moves_states = [(p, self.board.next_state(state, p)) for p in legal]
#
#             if all(plays.get((player, S)) for p, S in moves_states):
#                 # If we have stats on all of the legal moves here, use them.
#                 log_total = log(
#                     sum(plays[(player, S)] for p, S in moves_states))
#                 value, move, state = max(
#                     ((wins[(player, S)] / plays[(player, S)]) +
#                      self.C * sqrt(log_total / plays[(player, S)]), p, S)
#                     for p, S in moves_states
#                 )
#             else:
#                 # Otherwise, just make an arbitrary decision.
#                 move, state = choice(moves_states)
#
#             states_copy.append(state)
#
#             # `player` here and below refers to the player
#             # who moved into that particular state.
#             if expand and (player, state) not in plays:
#                 expand = False
#                 plays[(player, state)] = 0
#                 wins[(player, state)] = 0
#                 if t > self.max_depth:
#                     self.max_depth = t
#
#             visited_states.add((player, state))
#
#             player = self.board.current_player(state)
#             winner = self.board.winner(states_copy)
#             if winner:
#                 break
#
#         for player, state in visited_states:
#             if (player, state) not in plays:
#                 continue
#             plays[(player, state)] += 1
#             if player == winner:
#                 wins[(player, state)] += 1
#
#
# def monte_carlo_tree_search(root):
#     while resources_left(time, computational power):
#         leaf = traverse(root)
#         simulation_result = rollout(leaf)
#         backpropagate(leaf, simulation_result)
#
#     return best_child(root)
#
#
# # function for node traversal
# def traverse(node):
#     while fully_expanded(node):
#         node = best_uct(node)
#
#         # in case no children are present / node is terminal
#     return pick_univisted(node.children) or node
#
#
# # function for the result of the simulation
# def rollout(node):
#     while non_terminal(node):
#         node = rollout_policy(node)
#     return result(node)
#
#
# # function for randomly selecting a child node
# def rollout_policy(node):
#     return pick_random(node.children)
#
#
# # function for backpropagation
# def backpropagate(node, result):
#     if is_root(node) return
#     node.stats = update_stats(node, result)
#     backpropagate(node.parent)
#
#
# # function for selecting the best child
# # node with highest number of visits
# def best_child(node):
#     pick
#     child
#     with highest number of visits