import math
from game_logic import GameState

def minimax_with_alpha_beta_pruning(state, depth, alpha, beta, is_maximizing_player, ai_player):
    is_terminal, winner = state.is_terminal()
    if is_terminal or depth == 0:
        return evaluate(state, ai_player), None

    best_move = None
    if state.current_player == ai_player:
        max_eval = -math.inf
        for move in state.get_legal_moves():
            next_state = state.apply_move(move)
            eval, _ = minimax_with_alpha_beta_pruning(next_state, depth - 1, alpha, beta, False, ai_player)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in state.get_legal_moves():
            next_state = state.apply_move(move)
            eval, _ = minimax_with_alpha_beta_pruning(next_state, depth - 1, alpha, beta, True, ai_player)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def evaluate(state, maximizing_player):
    terminal, winner = state.is_terminal()
    if terminal:
        score = math.inf if winner == maximizing_player else -math.inf
        # print(f"[EVAL] Stan końcowy: Zwycięzca = {winner}, Ocena = {score}")
        return score

    row = state.neutron_pos[0]
    if maximizing_player == 'W':
        score = 4 - row
    else:
        score = row

    # print(f"[EVAL] Pozycja neutronu: {state.neutron_pos}, Gracz: {maximizing_player}, Ocena: {score}")
    return score

