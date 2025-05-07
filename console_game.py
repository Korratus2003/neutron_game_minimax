from game_logic import GameState


def print_board(board):
    print("  0 1 2 3 4")
    for r in range(5):
        print(r, end=" ")
        for c in range(5):
            print(board[r][c], end=" ")
        print()


def main():
    state = GameState(
        board=[
            ['W', 'W', 'W', 'W', 'W'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', 'N', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['B', 'B', 'B', 'B', 'B']
        ],
        neutron_pos=(2, 2),
        current_player='W'
    )

    while True:
        print("\n--- Current player:", state.current_player + " ---")
        print_board(state.board)

        terminal, winner = state.is_terminal()
        if terminal:
            print(f"\nGame over! Winner: {winner}")
            break

        moves = state.get_legal_moves()
        if not moves:
            print("No legal moves!")
            break

        print("\nNeutron position:", state.neutron_pos)
        print("Legal moves format: [neutron_row,neutron_col] [piece_row,piece_col] [move_row,move_col]")

        try:
            move = input("Enter move: ").split()
            neutron = tuple(map(int, move[0].split(',')))
            piece_from = tuple(map(int, move[1].split(',')))
            piece_to = tuple(map(int, move[2].split(',')))
            full_move = (neutron, (piece_from, piece_to))

            if full_move in moves:
                state = state.apply_move(full_move)
            else:
                print("Invalid move! Available moves:", moves)
        except:
            print("Invalid input format!")


if __name__ == "__main__":
    main()
    #pierwszy ruch to w jaką pozycje przesunąć N potem spacja pozycja pionka do przesunięcia spacja docelowa pozycja np 1,1 0,0 1,0
