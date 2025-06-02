import tkinter as tk
import math
from game_logic import GameState
from ai_minimax import minimax_with_alpha_beta_pruning


class NeutronGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Neutron")

        self.colors = {
            'W': '#4CAF50',
            'B': '#F44336',
            'N': '#808080'
        }

        self.canvas = tk.Canvas(self, width=400, height=400, bg='#EEE')
        self.canvas.pack(pady=20)

        self.status_label = tk.Label(self, text="Twój ruch: kliknij neutron", font=('Arial', 12))
        self.status_label.pack()

        tk.Button(self, text="Nowa gra", command=self.reset_game).pack(pady=10)

        self.phase = "neutron"
        self.selected_moves = []
        self.possible_moves = []
        self.temp_state = None

        self.canvas.bind("<Button-1>", self.handle_click)

        self.reset_game()
        self.draw_board()

    def reset_game(self):
        self.game_state = GameState(
            board=[
                ['W', 'W', 'W', 'W', 'W'],
                ['.', '.', '.', '.', '.'],
                ['.', '.', 'N', '.', '.'],
                ['.', '.', '.', '.', '.'],
                ['B', 'B', 'B', 'B', 'B'],
            ],
            neutron_pos=(2, 2),
            current_player='W'
        )
        self.temp_state = None
        self.phase = "neutron"
        self.selected_moves = []
        self.possible_moves = []
        self.update_status()
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        current_state = self.temp_state if self.temp_state else self.game_state

        for r in range(5):
            for c in range(5):
                x0, y0 = c * 80, r * 80
                x1, y1 = x0 + 80, y0 + 80
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="#999")

                piece = current_state.board[r][c]
                if piece in self.colors:
                    self.canvas.create_oval(x0 + 15, y0 + 15, x1 - 15, y1 - 15,
                                            fill=self.colors[piece], outline="#333", width=2)

                if (r, c) in self.possible_moves:
                    self.canvas.create_rectangle(x0, y0, x1, y1, outline="blue", width=3)

                if self.phase == "neutron" and (r, c) == current_state.neutron_pos:
                    self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", width=3)

    def handle_click(self, event):
        if self.game_state.current_player != 'W' or self.phase == "game_over":
            return

        col = event.x // 80
        row = event.y // 80
        pos = (row, col)

        if self.phase == "neutron":
            if pos == self.game_state.neutron_pos:
                self.possible_moves = [m[0] for m in self.game_state.get_legal_moves()]
                if not self.possible_moves:
                    self.end_game("Czerwony")
                    return
                self.phase = "neutron_move"
                self.update_status("Wybierz nową pozycję neutronu")
                self.draw_board()

        elif self.phase == "neutron_move":
            if pos in self.possible_moves:
                self.temp_state = self.game_state.apply_move((pos, None))
                self.animate_move(self.game_state.neutron_pos, pos, 'N')
                self.phase = "piece"
                self.selected_moves = [pos]
                self.possible_moves = self.temp_state.get_own_pieces(self.temp_state.board)
                self.update_status("Wybierz swój pionek")
                self.draw_board()

        elif self.phase == "piece":
            if pos in self.possible_moves:
                self.selected_moves.append(pos)
                self.possible_moves = self.temp_state.get_piece_moves(pos)
                if not self.possible_moves:
                    self.end_game("Czerwony")
                    return
                self.phase = "piece_move"
                self.update_status("Wybierz nową pozycję pionka")
                self.draw_board()

        elif self.phase == "piece_move":
            if pos in self.possible_moves:
                full_move = (self.selected_moves[0], (self.selected_moves[1], pos))
                self.animate_move(self.selected_moves[1], pos, 'W')
                self.game_state = self.game_state.apply_move(full_move)
                self.finalize_move()

    def animate_move(self, frm, to, piece_type):
        steps = 10
        fr, fc = frm
        tr, tc = to

        x0 = fc * 80 + 40
        y0 = fr * 80 + 40
        x1 = tc * 80 + 40
        y1 = tr * 80 + 40
        dx = (x1 - x0) / steps
        dy = (y1 - y0) / steps

        self.canvas.create_oval(fc * 80 + 15, fr * 80 + 15, fc * 80 + 65, fr * 80 + 65,
                                fill='#EEE', outline='#EEE')

        obj = self.canvas.create_oval(x0 - 25, y0 - 25, x0 + 25, y0 + 25,
                                      fill=self.colors[piece_type],
                                      outline="#333")

        def update(i):
            if i <= steps:
                self.canvas.move(obj, dx, dy)
                self.after(30, update, i + 1)
            else:
                self.canvas.delete(obj)
                self.draw_board()

        update(1)

    def finalize_move(self):
        self.temp_state = None
        self.phase = "neutron"
        self.selected_moves = []
        self.possible_moves = []
        self.draw_board()
        self.check_turn()

    def check_turn(self):
        terminal, winner = self.game_state.is_terminal()
        if terminal:
            self.end_game("Zielony" if winner == 'W' else "Czerwony")
        elif self.game_state.current_player == 'B':
            self.update_status("Ruch przeciwnika")
            self.after(1000, self.ai_move)
        else:
            self.update_status()

    def ai_move(self):
        score, move = minimax_with_alpha_beta_pruning(self.game_state, 3, -math.inf, math.inf, True, 'B')
        if move:
            nm, pm = move
            print(f"[AI MOVE] Ocena: {score}, Ruch: neutron {nm}, pionek {pm}")
            self.animate_move(self.game_state.neutron_pos, nm, 'N')
            if pm:
                self.animate_move(pm[0], pm[1], 'B')
            self.game_state = self.game_state.apply_move(move)
            self.after(700, self.check_turn)
        else:
            self.end_game("Zielony")

    def end_game(self, winner):
        self.status_label.config(text=f"Koniec gry! Zwycięzca: {winner}")
        self.phase = "game_over"

    def update_status(self, text=None):
        status_texts = {
            "neutron": "Twój ruch: kliknij neutron",
            "neutron_move": "Wybierz nową pozycję neutronu",
            "piece": "Wybierz swój pionek",
            "piece_move": "Wybierz nową pozycję pionka"
        }
        self.status_label.config(text=text if text else status_texts.get(self.phase, ""))


if __name__ == "__main__":
    app = NeutronGUI()
    app.mainloop()
