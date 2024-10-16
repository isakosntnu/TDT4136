State = tuple[int, list[str | int]]  # Tuple of player (whose turn it is),
                                     # and the buckets (as str)
                                     # or the number in a bucket
Action = str | int  # Bucket choice (as str) or choice of number


class Game:
    def initial_state(self) -> State:
        return 0, ['A', 'B', 'C']

    def to_move(self, state: State) -> int:
        player, _ = state
        return player

    def actions(self, state: State) -> list[Action]:
        _, actions = state
        return actions

    def result(self, state: State, action: Action) -> State:
        if action == 'A':
            return (self.to_move(state) + 1) % 2, [-50, 50]
        elif action == 'B':
            return (self.to_move(state) + 1) % 2, [3, 1]
        elif action == 'C':
            return (self.to_move(state) + 1) % 2, [-5, 15]
        assert type(action) is int
        return (self.to_move(state) + 1) % 2, [action]

    def is_terminal(self, state: State) -> bool:
        _, actions = state
        return len(actions) == 1

    def utility(self, state: State, player: int) -> float:
        assert self.is_terminal(state)
        _, actions = state
        assert type(actions[0]) is int
        return actions[0] if player == self.to_move(state) else -actions[0]

    def print(self, state):
        print(f'The state is {state} and ', end='')
        if self.is_terminal(state):
            print(f'P1\'s utility is {self.utility(state, 0)}')
        else:
            print(f'it is P{self.to_move(state)+1}\'s turn')
            
def minimax_search(game, state):
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


# Play the game
game = Game()
state = game.initial_state()
game.print(state)

while not game.is_terminal(state):
    player = game.to_move(state)
    action = minimax_search(game, state)  # The player whose turn it is uses the Minimax algorithm
    print(f'P{player + 1}\'s action: {action}')
    assert action is not None
    state = game.result(state, action)
    game.print(state)
