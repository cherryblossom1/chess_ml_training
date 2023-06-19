import chess
from chess import pgn
import sys
import re

# Parse moves from the text input and convert to moves object
def process_game(game):
    moves = re.findall(r'\d+\.\s+(\S+)', game)
    return moves

# read N games
Nread=2
read_count=0
current_game = ''
moves_dataset = []
unique_moves = set()
for line in sys.stdin:
    # Detect the start of a new game if counter is not exceeded
    if line.startswith('[Event'):
        if read_count == Nread+1:
            break
        # increment game counter
        read_count += 1
        # process the current game
        pgn_moves = process_game(current_game)
        if pgn_moves:
            moves_dataset.append(pgn_moves)
            unique_moves.update(pgn_moves)
        # start fresh game
        current_game = ''
    # Append the current line to the current game
    current_game += line

# total unique moves so far
unique_move_count = len(unique_moves)
