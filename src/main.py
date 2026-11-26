import chess


def play_game():
    board = chess.Board()
    print("Enter moves like e4 or Nf3. Type 'done' to finish.")

    while True:
        # Showing whose turn it is so I don't lose track mid-game
        side = "White" if board.turn == chess.WHITE else "Black"
        text = input(f"{side} move: ").strip()

        if text.lower() == "done":
            break

        try:
            # parse_san already rejects illegal moves, so no manual rule checking
            move = board.parse_san(text)
        except ValueError:
            print("Illegal or unreadable move, try again.")
            continue

        board.push(move)

    return board


if __name__ == "__main__":
    play_game()