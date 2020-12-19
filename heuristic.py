import copy
import math
import random
import time


class MonteCarlo:

    def __init__(self, checkers, color, sim_time=1, exp_time=1, bias=0.1):
        self._color = color
        self._oposite_color = 'BLACK' if color == 'RED' else 'RED'
        self._sim_time = sim_time  # Simulation time
        self._state_node = {}  # Game state tree
        self._exp_time = exp_time  # Exploration value
        self._bias = bias  # Pre-tuned bias constant
        self._checkers = checkers

    def static_concentric_val(self, game_state, king_coefficient=20):

        def concentric_coefficient(b, pos):

            if pos[0] == 0 or pos[0] == len(b.get_board()) - 1:
                return 5
            elif pos[1] == 0 or pos[1] == len(b.get_board()[0]) - 1:
                return 4
            elif (pos[0] == 1 or pos[0] == 6) and (pos[1] <= 6 or pos[1] >= 1):
                return 3
            elif (pos[1] == 1 or pos[1] == 6) and (pos[0] <= 6 or pos[0] >= 1):
                return 3
            elif (pos[0] == 2 or pos[0] == 5) and (pos[1] <= 5 or pos[1] >= 2):
                return 2
            elif (pos[1] == 2 or pos[1] == 5) and (pos[0] <= 5 or pos[0] >= 2):
                return 2
            else:
                return 1

        # Count the number of discs of the player's color,
        # and reward for kings. Subtract the opponent toll.

        board = game_state

        play = 0
        oppo = 0

        for i, row in enumerate(board.get_board()):
            for j, char in enumerate(row):
                if char == self._color.lower():
                    play += 3 + concentric_coefficient(board, (i, j))
                # if char == color.upper():
                #     play += king_coefficient

                if char == self._checkers.opponent(self._color).lower():
                    oppo += 3 + concentric_coefficient(board, (i, j))
                # if char == self.checkers.opponent(color).upper():
                #     oppo += king_coefficient

        return play - oppo

    def monte_carlo_search(self, game_state):
        """
        Returns best action w. Monte-Carlo Tree Search + Upper Confidence Bound.
        :param game_state:
        :return:
        """

        results = {}

        if game_state in self._state_node:
            root = self._state_node[game_state]
        else:
            n_children = len(self._checkers.get_possible_moves())
            root = Node(game_state, None, n_children)

        # Remove its parent as it is now considered our root level node.

        root.parent = None

        sim_count = 0
        now = time.time()
        while time.time() - now < self._sim_time and root.moves_unfinished > 0:
            print("time")
            print(time.time() - now)
            print("/time")

            picked_node = self.tree_policy(root)
            result, actions = self.simulate(picked_node.game_state)
            self.back_prop(picked_node, result, actions, player=picked_node.game_state[1])
            sim_count += 1

        for child in root.children:
            wins, plays = child.get_wins_plays()
            position = child.move

            results[tuple(position)] = (wins, plays)
        return self.best_action(root)

    @staticmethod
    def best_action(node):

        most_plays = -float('inf')
        best_wins = -float('inf')
        best_actions = []
        for child in node.children:
            wins, plays = child.get_wins_plays()

            if plays > most_plays:
                most_plays = plays
                best_actions = [child.move]
                best_wins = wins
            elif plays == most_plays:
                # break ties with wins
                if wins > best_wins:
                    best_wins = wins
                    best_actions = [child.move]
                elif wins == best_wins:
                    best_actions.append(child.move)

        return random.choice(best_actions)

    # node, result(1 if win, 05 draw 0 lose), actions - sequence of moves, player color
    @staticmethod
    def back_prop(node, delta, actions, player):

        t = 0
        while node.parent is not None:
            node.plays += 1
            node.wins += delta

            for u in range(t, len(actions[player])):
                if actions[player][u] not in actions[player][t:u]:
                    node.amaf_plays += 1
                    node.amaf_wins += delta

            t += 1
            node = node.parent

        node.plays += 1
        node.wins += delta

        for u in range(t, len(actions[player])):
            if actions[player][u] not in actions[player][t:u]:
                node.amaf_plays += 1
                node.amaf_wins += delta

    # REWRITTEN
    def tree_policy(self, node):
        while True and not node.game_state.is_board_over:

            legal_moves = node.game_state.get_possible_moves()

            if len(node.children) < len(legal_moves):

                unexpanded = [
                    move for move in legal_moves
                    if tuple(move) not in node.moves_expanded
                ]

                assert len(unexpanded) > 0
                move = random.choice(unexpanded)

                next_state = copy.deepcopy(node.game_state)
                next_state.move(move)

                child = Node(next_state, move, len(legal_moves))
                node.add_child(child)
                self._state_node[next_state] = child

                return child

            else:
                # Every possible next state has been expanded, pick one.
                cur_node = self.best_child(node)

        return node

    def best_child(self, node):

        enemy_turn = (node.color != self._color)
        values = {}

        for child in node.children:
            wins, plays = child.get_wins_plays()
            a_wins, a_plays = child.get_amaf_wins_plays()

            if enemy_turn:
                wins = plays - wins
                a_wins = a_plays - a_wins

            _, parent_plays = node.get_wins_plays()
            beta = node.get_beta(self._bias)

            if a_plays > 0:
                values[child] = (1 - beta) * (wins / plays) + beta * (a_wins / a_plays) \
                                + self._exp_time * math.sqrt(2 * math.log(parent_plays) / plays)
            else:
                values[child] = (wins / plays) + self._exp_time * math.sqrt(2 * math.log(parent_plays) / plays)

        best_choice = max(values, key=values.get)
        return best_choice

    # REWRITTEN
    def simulate(self, game_state):

        actions = {self._color: [], self._oposite_color: []}
        state = copy.deepcopy(game_state)

        while True:
            result = state.is_board_over()
            if result:
                winner = state.get_board_winner()
                if winner == self._color:
                    return 1, actions
                elif winner == self._oposite_color:
                    return 0, actions
                else:
                    return .5, actions

            moves = state.get_possible_moves()

            try:
                picked = random.choice(moves)
            except BaseException:
                print("e")

            actions[self._color].append(picked)

            state.move(picked)


# REWRITTEN
class Node:

    def __init__(self, game_state, move, amount_children):

        self.game_state = game_state
        self.color = game_state.whose_turn()
        self.plays = 0
        self.wins = 0
        self.amount_of_plays = 0
        self.amount_of_wins = 0
        self.children = []
        self.parent = None
        self.moves_expanded = set()  # which moves have we tried at least once
        self.moves_unfinished = amount_children  # amount of moves not fully expanded
        self.move = move

    def propagate_completion(self):

        if self.parent is None:
            return

        if self.moves_unfinished > 0:
            self.moves_unfinished -= 1

        self.parent.propagate_completion()

    def add_child(self, node):
        self.children.append(node)
        self.moves_expanded.add(tuple(node.move))
        node.parent = self

    def has_children(self):
        return len(self.children) > 0

    def get_wins_plays(self):
        return self.wins, self.plays

    def get_beta(self, b):
        return self.amount_of_plays / (self.plays + self.amount_of_plays +
                                       4 * self.plays * self.amount_of_plays * pow(b, 2))
