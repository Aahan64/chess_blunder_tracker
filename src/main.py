import shutil
import sys

import chess
import chess.engine

THINK_TIME = 0.1    # seconds per position, fast enough that typing moves never feels slow
BLUNDER_DROP = 150  # about a pawn and a half, my personal line for a real blunder


def start_engine():
    path = shutil.which("stockfish")
    if path is None:
        print("Stockfish not found. Install it with: brew install stockfish")
        sys.exit(1)
    return chess.engine.SimpleEngine.popen_uci(path)


def get_eval(engine, board, my_color):
    info = engine.analyse(board, chess.engine.Limit(time=THINK_TIME))
    # Score from my side, so a lower number always means I got worse
    return info["score"].pov(my_color).score(mate_score=10000)


def get_phase(move_number):
    # I picked these cutoffs from how my own games usually go
    if move_number <= 15:
        return "opening"
    if move_number <= 35:
        return "middlegame"
    return "endgame"


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

        # Save these before pushing, because the board changes after
        is_my_move = board.turn == my_color
        move_number = board.fullmove_number
        move_text = board.san(move)
        board.push(move)

        new_eval = get_eval(engine, board, my_color)

        # Only my moves count, I'm tracking my mistakes, not my opponent's
        if is_my_move and last_eval - new_eval > BLUNDER_DROP:
            phase = get_phase(move_number)
            print(f"Blunder! Eval dropped {last_eval - new_eval} cp ({phase})")
            blunders.append({"move_number": move_number, "move": move_text, "phase": phase})

        last_eval = new_eval

    return blunders


if __name__ == "__main__":
    engine = start_engine()
    try:
        found = play_game(engine)
        print(f"Blunders this game: {len(found)}")
        for blunder in found:
            print(f"Move {blunder['move_number']}: {blunder['move']} ({blunder['phase']})")
    finally:
        engine.quit()