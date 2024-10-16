from copy import deepcopy
import time

State = tuple[int, list[list[int | None]]]  # Tuple of player (whose turn it is), and board
Action = tuple[int, int]  # Where to place the player's piece

class Game:
    def initial_state(self) -> State:
        return (0, [[None, None, None], [None, None, None], [None, None, None]])

    def to_move(self, state: State) -> int:
        player_index, _ = state
        return player_index

    def actions(self, state: State) -> list[Action]:
        _, board = state
        actions = []
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    actions.append((row, col))
        return actions

    def result(self, state: State, action: Action) -> State:
        _, board = state
        row, col = action
        next_board = deepcopy(board)
        next_board[row][col] = self.to_move(state)
        return (self.to_move(state) + 1) % 2, next_board

    def is_winner(self, state: State, player: int) -> bool:
        _, board = state
        for row in range(3):
            if all(board[row][col] == player for col in range(3)):
                return True
        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        return all(board[i][2 - i] == player for i in range(3))

    def is_terminal(self, state: State) -> bool:
        _, board = state
        if self.is_winner(state, (self.to_move(state) + 1) % 2):
            return True
        return all(board[row][col] is not None for row in range(3) for col in range(3))

    def utility(self, state, player):
        assert self.is_terminal(state)
        if self.is_winner(state, player):
            return 1
        if self.is_winner(state, (player + 1) % 2):
            return -1
        return 0

    def print(self, state: State):
        _, board = state
        print()
        for row in range(3):
            cells = [
                ' ' if board[row][col] is None else 'x' if board[row][col] == 0 else 'o'
                for col in range(3)
            ]
            print(f' {cells[0]} | {cells[1]} | {cells[2]}')
            if row < 2:
                print('---+---+---')
        print()
        if self.is_terminal(state):
            if self.utility(state, 0) > 0:
                print(f'P1 won')
            elif self.utility(state, 1) > 0:
                print(f'P2 won')
            else:
                print('The game is a draw')
        else:
            print(f'It is P{self.to_move(state)+1}\'s turn to move')



def minimax_search(game, state):
    # YOUR CODE HERE
    player = game.to_move(state)
    value, move = max_value(game, state, player)
    return move

def max_value(game, state, player):
    if game.is_terminal(state):
        return game.utility(state, player), None

    v = -float('inf')
    best_action = None
    for action in game.actions(state):
        min_val, _ = min_value(game, game.result(state, action), player)
        if min_val > v:
            v = min_val
            best_action = action
    return v, best_action

def min_value(game, state, player):
    if game.is_terminal(state):
        return game.utility(state, player), None

    v = float('inf')
    best_action = None
    for action in game.actions(state):
        max_val, _ = max_value(game, game.result(state, action), player)
        if max_val < v:
            v = max_val
            best_action = action
    return v, best_action


# Alpha-beta code
def alpha_beta_search(game, state):
    player = game.to_move(state)
    value, move = max_value_alpha_beta(game, state, player, -float('inf'), float('inf'))
    return move

def max_value_alpha_beta(game, state, player, alpha, beta):
    if game.is_terminal(state):
        return game.utility(state, player), None

    v = -float('inf')
    best_action = None
    for action in game.actions(state):
        min_val, _ = min_value_alpha_beta(game, game.result(state, action), player, alpha, beta)
        if min_val > v:
            v = min_val
            best_action = action
        # Update alpha, this is the best score we can guarantee so far
        alpha = max(alpha, v)
        
        # Beta cutoff: if our current max value is >= beta, opponent would not let us reach here
        # The minimizing player has a guaranteed better option, so skip remaining actions
        if v >= beta:
            break
    return v, best_action

def min_value_alpha_beta(game, state, player, alpha, beta):
    if game.is_terminal(state):
        return game.utility(state, player), None

    v = float('inf')
    best_action = None
    for action in game.actions(state):
        max_val, _ = max_value_alpha_beta(game, game.result(state, action), player, alpha, beta)
        if max_val < v:
            v = max_val
            best_action = action
         # Update beta, this is the best score opponent can guarantee so far
        beta = min(beta, v)
        
        # Alpha cutoff: if our current min value is <= alpha, we (minimizing player) will never go here
        #the maximizing player has found a guaranteed better path, so skip remaining actions
        if v <= alpha:
            break
    return v, best_action


# Timing and comparing Minimax and Alpha-beta pruning
game = Game()
state = game.initial_state()

# Timing Minimax
# start_time_minimax = time.time()
# minimax_move = minimax_search(game, state)
# minimax_time = time.time() - start_time_minimax

# # Timing Alpha-beta pruning
# start_time_alpha_beta = time.time()
# alpha_beta_move = alpha_beta_search(game, state)
# alpha_beta_time = time.time() - start_time_alpha_beta
# print(f"Minimax move: {minimax_move}, Time taken: {minimax_time:.4f} seconds")
# print(f"Alpha-beta move: {alpha_beta_move}, Time taken: {alpha_beta_time:.4f} seconds")

# Play using Alpha-beta pruning (You can change this to minimax_search to compare in action)
while not game.is_terminal(state):
    player = game.to_move(state)
    #action = minimax_search(game, state)  
    action = alpha_beta_search(game, state)  
    print(f'P{player + 1}\'s action: {action}')
    assert action is not None
    state = game.result(state, action)
    game.print(state)  # Print the current board after each move
