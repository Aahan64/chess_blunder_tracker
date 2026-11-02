# Chess Blunder Tracker

## Project Goal
I play chess professionally , and after every game I know I blundered but not why, or whether it's the same mistake again and again. This is a Python command-line tool where I enter my games move by move, and it uses Stockfish to flag my blunders. After 10 or more games, it shows which phase of the game I blunder in most, so I know what to train.

## MVP Scope
- Enter moves one by one, with illegal moves rejected
- Stockfish evaluates every position
- Flag my moves where the eval drops by more than 150 centipawns
- Label each blunder as opening (moves 1-15), middlegame (16-35), or endgame (36+)
- Save games to `games.json`
- After 10 games, report blunders per phase

## Future Plans (V2.0+)
- Blunder type (hung piece, missed tactic, other) should be displayed as well
- Import games from PGN files
- Charts of blunder trends over time
- Filter the report by color, opening, or opponent rating

## Tech Stack
- Python 3
- python-chess
- Stockfish (local engine)
- json (built in) for storage
- Git and GitHub

## Docs
- [Eisenhower Matrix](Eisenhower_Matrix.pdf)
- [System Diagram](System_Diagram.png)

