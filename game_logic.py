class GameState:
    def __init__(self, board, neutron_pos, current_player):
        self.board = [list(row) for row in board]
        self.neutron_pos = neutron_pos
        self.current_player = current_player

    def get_legal_moves(self):
        moves = []
        neutron_moves = self._get_sliding_moves(self.neutron_pos)

        for nm in neutron_moves:
            temp_board = self.apply_neutron_move(nm)
            for piece in self._get_own_pieces(temp_board):
                piece_moves = self._get_sliding_moves(piece, temp_board)
                for pm in piece_moves:
                    moves.append((nm, (piece, pm)))

        print("Legal moves:", moves)  # DEBUG
        return moves

    def _get_sliding_moves(self, pos, board=None):
        board = board or self.board
        r, c = pos
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while 0 <= nr < 5 and 0 <= nc < 5 and board[nr][nc] == '.':
                moves.append((nr, nc))
                nr += dr
                nc += dc
        return moves

    def apply_neutron_move(self, new_pos):
        new_board = [row.copy() for row in self.board]
        old_r, old_c = self.neutron_pos
        new_r, new_c = new_pos
        new_board[old_r][old_c] = '.'
        new_board[new_r][new_c] = 'N'
        return new_board

    def _get_own_pieces(self, board):
        return [(r, c) for r in range(5) for c in range(5) if board[r][c] == self.current_player]

    def apply_move(self, move):
        neutron_move, piece_move = move
        new_board = self.apply_neutron_move(neutron_move)

        if piece_move:
            (from_r, from_c), (to_r, to_c) = piece_move
            if new_board[to_r][to_c] == '.':  # Sprawdzenie czy ruch jest możliwy
                new_board[from_r][from_c] = '.'
                new_board[to_r][to_c] = self.current_player
            else:
                print("Invalid piece move!")

        new_player = 'B' if self.current_player == 'W' else 'W'
        return GameState(new_board, neutron_move, new_player)

    def is_terminal(self):
        if self.neutron_pos[0] == 0:
            return True, 'W'
        if self.neutron_pos[0] == 4:
            return True, 'B'
        return False, None