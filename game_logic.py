import copy

class GameState:
    def __init__(self, board, neutron_pos, current_player):
        self.board = [list(row) for row in board]
        self.neutron_pos = neutron_pos
        self.current_player = current_player

    def get_legal_moves(self):
        moves = []
        neutron_moves = self.get_piece_moves(self.neutron_pos)

        for nm in neutron_moves:
            if self.is_winning_neutron_move(nm):
                moves.append((nm, None))
                continue

            temp_board = self.apply_neutron_move(nm)
            own_pieces = self.get_own_pieces(temp_board)

            for piece in own_pieces:
                piece_moves = self.get_piece_moves(piece, temp_board)
                for pm in piece_moves:
                    moves.append((nm, (piece, pm)))

        return moves

    def get_piece_moves(self, pos, board=None):
        if board is None:
            board = self.board
        r, c = pos
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            last_valid = None
            while 0 <= nr < 5 and 0 <= nc < 5:
                if board[nr][nc] != '.':
                    break
                last_valid = (nr, nc)
                nr += dr
                nc += dc
            if last_valid and last_valid != (r, c):
                moves.append(last_valid)
        return moves

    def apply_neutron_move(self, new_pos):
        new_board = copy.deepcopy(self.board)
        old_r, old_c = self.neutron_pos
        new_r, new_c = new_pos
        new_board[old_r][old_c] = '.'
        new_board[new_r][new_c] = 'N'
        return new_board

    def get_own_pieces(self, board):
        return [(r, c) for r in range(5) for c in range(5) if board[r][c] == self.current_player]

    def is_winning_neutron_move(self, pos):
        return (self.current_player == 'W' and pos[0] == 0) or (self.current_player == 'B' and pos[0] == 4)

    def apply_move(self, move):
        neutron_move, own_move = move
        new_board = self.apply_neutron_move(neutron_move)

        next_player = self.current_player
        if own_move:
            (from_pos, to_pos) = own_move
            new_board[from_pos[0]][from_pos[1]] = '.'
            new_board[to_pos[0]][to_pos[1]] = self.current_player
            next_player = 'B' if self.current_player == 'W' else 'W'
        elif self.is_winning_neutron_move(neutron_move):
            next_player = None

        return GameState(new_board, neutron_move, next_player)

    def is_terminal(self):
        if self.neutron_pos[0] == 0:
            return True, 'W'
        if self.neutron_pos[0] == 4:
            return True, 'B'

        if not self.get_piece_moves(self.neutron_pos):
            return True, 'B' if self.current_player == 'W' else 'W'

        if not self.get_legal_moves():
            return True, 'B' if self.current_player == 'W' else 'W'

        return False, None
