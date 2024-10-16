import math

State = tuple[int, int] # Tuple of player (whose turn it is),
                        # and the number to be decreased
Action = str  # Decrement (number <- number-1) or halve (number <- number / 2)

class Game:
    def __init__(self, N: int):
        self.N = N

    def initial_state(self) -> State:
        return 0, self.N

    def to_move(self, state: State) -> int:
        player, _ = state
        return player

    def actions(self, state: State) -> list[Action]:
        return ['--', '/2']

    def result(self, state: State, action: Action) -> State:
        _, number = state
        if action == '--':
            return (self.to_move(state) + 1) % 2, number - 1
        else:
            return (self.to_move(state) + 1) % 2, number // 2  # Floored division

    def is_terminal(self, state: State) -> bool:
        _, number = state
        return number == 0

    def utility(self, state: State, player: int) -> float:
        assert self.is_terminal(state)
        return 1 if self.to_move(state) == player else -1

    def print(self, state: State):
        _, number = state
        print(f'The number is {number} and ', end='')
        if self.is_terminal(state):
            if self.utility(state, 0) > 0:
                print(f'P1 won')
            else:
                print(f'P2 won')
        else:
            print(f'it is P{self.to_move(state)+1}\'s turn')

def minimax_search(game, state):
    # YOUR CODE HERE
    #Find whos turn it is and call max_value to find the best move
    player = game.to_move(state)
    value, move = max_value(game, state, player)  
    return move


def max_value(game, state, player):
    # check if game is over
    if game.is_terminal(state):
        return game.utility(state, player), None

    #set negativie infinitiy values so that we easily can update it with max value
    v = -float('inf')
    best_action = None
    
    #Loop through all possible actions and find the best action 
    for action in game.actions(state):
        min_val, _ = min_value(game, game.result(state, action), player)
        if min_val > v:
            v = min_val
            best_action = action
    
    #returns the best value and the best action
    return v, best_action


def min_value(game, state, player):
    #Does the same as max_value but with the opposite values and it tries to find the minimum value
    if game.is_terminal(state):
        return game.utility(state, player), None
    
    
    #instead of negative infinity we use positive infinity
    v = float('inf')
    best_action = None
    
    #loops through and in stead of finding the max value it tries to find the minimum value
    for action in game.actions(state):
        max_val, _ = max_value(game, game.result(state, action), player)
        if max_val < v:
            v = max_val
            best_action = action
            
    #Returns lovest value and action
    return v, best_action


game = Game(5)

state = game.initial_state()
game.print(state)
while not game.is_terminal(state):
    player = game.to_move(state)
    action = minimax_search(game, state) # The player whose turn it is
                                         # is the MAX player
    print(f'P{player+1}\'s action: {action}')
    assert action is not None
    state = game.result(state, action)
    game.print(state)

# Expected output:
# The number is 5 and it is P1's turn
# P1's action: --
# The number is 4 and it is P2's turn
# P2's action: --
# The number is 3 and it is P1's turn
# P1's action: /2
# The number is 1 and it is P2's turn
# P2's action: --
# The number is 0 and P1 won
