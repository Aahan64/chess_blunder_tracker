import shutil
import sys

import chess
import chess.engine

ENGINE_TIME = 0.1


def start_engine():
    path = shutil.which("stockfish")
    if path is None:
        print("Stockfish not found. Install it with: brew install stockfish")
        sys.exit(1)
    return chess.engine.SimpleEngine.popen_uci(path)


def evaluate(engine, board):
    info = engine.analyse(board, chess.engine.Limit(time=ENGINE_TIME))
    # Mate has no centipawn value, so I turn it into a huge number to keep the math simple
    return info["score"].white().score(mate_score=10000)


def play_game(engine):
    board = chess.Board()
    print("Enter moves like e4 or Nf3. Type 'done' to finish.")
    print("Use capital letters for pieces (Q, N, B, R, K).")

    while True:
        side = "White" if board.turn == chess.WHITE else "Black"
        text = input(f"{side} move: ").strip()

        if text.lower() == "done":
            break

        try:
            # parse_san already rejects illegal moves
            move = board.parse_san(text)
        except ValueError:
            print("Illegal or unreadable move, try again.")
            continue

        board.push(move)
        print(f"  Eval: {evaluate(engine, board)} centipawns (from White's side)")

    return board


if __name__ == "__main__":
    engine = start_engine()
    try:
        play_game(engine)
    finally:
        # Always need to shut Stockfish down
        engine.quit()