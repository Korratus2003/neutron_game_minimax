import math
from game_logic import GameState

def minimax(state, depth, is_maximizing):
    if depth == 0 or state.is_terminal()[0]:
        return evaluate(state), None

    if is_maximizing:
        best_val = -math.inf
        best_move = None
        for move in state.get_legal_moves():
            new_state = state.apply_move(move)
            val, _ = minimax(new_state, depth-1, False)
            if val > best_val:
                best_val = val
                best_move = move
        return best_val, best_move
    else:
        best_val = math.inf
        best_move = None
        for move in state.get_legal_moves():
            new_state = state.apply_move(move)
            val, _ = minimax(new_state, depth-1, True)
            if val < best_val:
                best_val = val
                best_move = move
        return best_val, best_move

def evaluate(state):
    terminal, winner = state.is_terminal()
    if terminal:
        return math.inf if winner == 'B' else -math.inf
    return state.neutron_pos[0]  # Im niższy rząd (B), tym lepiej dla AI