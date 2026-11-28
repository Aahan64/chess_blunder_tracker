import shutil
import sys

import chess
import chess.engine

# 0.1 seconds per position is quick enough to type fast, deep enough to catch real mistakes
THINK_TIME = 0.1

# 150 centipawns is roughly a pawn and a half, which is where a slip becomes a blunder
BLUNDER_DROP = 150


def start_engine():
    path = shutil.which("stockfish")
    if path is None:
        print("Stockfish not found. Install it with: brew install stockfish")
        sys.exit(1)
    return chess.engine.SimpleEngine.popen_uci(path)


def get_eval(engine, board, my_color):
    info = engine.analyse(board, chess.engine.Limit(time=THINK_TIME))
    # pov() gives the score from my side, so a lower number always means I got worse
    # mate has no centipawn value, so I treat it as a huge number
    return info["score"].pov(my_color).score(mate_score=10000)


def ask_color():
    while True:
        answer = input("Are you White or Black? (w/b): ").strip().lower()
        if answer == "w":
            return chess.WHITE
        if answer == "b":
            return chess.BLACK
        print("Type w or b.")


def play_game(engine):
    my_color = ask_color()
    board = chess.Board()
    blunders = []
    print("Enter moves like e4 or Nf3. Use capitals for pieces. Type 'done' to finish.")

    last_eval = get_eval(engine, board, my_color)

    while True:
        side = "White" if board.turn == chess.WHITE else "Black"
        text = input(f"{side} move: ").strip()

        if text.lower() == "done":
            break

        try:
            move = board.parse_san(text)
        except ValueError:
            print("Illegal or unreadable move, try again.")
            continue

        # Grab these before pushing, since the board changes after
        is_my_move = board.turn == my_color
        move_number = board.fullmove_number
        move_text = board.san(move)
        board.push(move)

        new_eval = get_eval(engine, board, my_color)

        # Only my moves count, the opponent's mistakes aren't what I'm tracking
        if is_my_move and last_eval - new_eval > BLUNDER_DROP:
            print(f"Blunder! Eval dropped {last_eval - new_eval} cp")
            blunders.append({"move_number": move_number, "move": move_text})

        last_eval = new_eval

    return blunders


if __name__ == "__main__":
    engine = start_engine()
    try:
        found = play_game(engine)
        print(f"Blunders this game: {len(found)}")
        for blunder in found:
            print(f"Move {blunder['move_number']}: {blunder['move']}")
    finally:
        engine.quit()