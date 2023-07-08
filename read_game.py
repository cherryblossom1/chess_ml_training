import sys
import re
import numpy as np
import random

# assign frequencies
def assign_random_freq(unique_moves,freq_mat):
    move_frequencies = dict()
    for move in unique_moves:
        frequency = random.choice(freq_mat)
        move_frequencies[move] = frequency
    return move_frequencies

# dissonance cost function
def calculate_dissonance(freq):
    dissonance = 0.0
    for i in range(len(freq)):
        for j in range(i+1, len(freq)):
            # Calculate the frequency ratio between two notes
            ratio = freq[j] / freq[i]
            # Calculate the dissonance score based on the frequency ratio
            dissonance += abs(1.0 - ratio)
    return dissonance

# Parse moves from the text input and convert to moves object
def process_game(game):
    moves = re.findall(r'\d+\.\s+(\S+)', game)
    return moves

# Path to the unique moves file
unique_moves_file = 'unique_moves.txt'

# read unique moves from file
move_freq_dict={}
with open(unique_moves_file,'r') as file:
    for line in file:
        move,freq = line.strip().split(':')
        move_freq_dict[move] = float(freq)

# generate frequencies
base_freq = 440
freq_mat = base_freq*2.0**(np.arange(-12,25)/12)

# read N games
#Nread=5
read_count=0
current_game = ''
moves_dataset = []
print('Parsing games...')
for line in sys.stdin:
    # Detect the start of a new game if counter is not exceeded
    if line.startswith('[Event'):
        #if read_count == Nread+1:
            #break
        # increment game counter
        read_count += 1
        print(f'Game {read_count}')
        # process the current game
        pgn_moves = process_game(current_game)
        if pgn_moves:
            moves_dataset.append(pgn_moves)
            # Update move-frequency mappings
            for move in pgn_moves:
                if move not in move_freq_dict:
                    move_freq_dict[move] = random.choice(freq_mat)
            with open(unique_moves_file,'w') as file:
                for move,freq in move_freq_dict.items():
                    file.write(f'{move}:{freq}\n')
        # start fresh game
        current_game = ''
    # Append the current line to the current game
    current_game += line

Nread = read_count-1
# list of unique moves
unique_moves = list(move_freq_dict.keys())

# parse through given dataset to obtain frequency assignment for minimum dissonance
min_dissonance=90
move_frequencies = move_freq_dict
Nruns=100
for game_number in range(Nread):
    run_count=0
    while(run_count < Nruns):
        game_moves = moves_dataset[game_number]
        freq_moves = [move_frequencies[key] for key in game_moves]
        dissonance = calculate_dissonance(freq_moves)
        if(dissonance < min_dissonance):
            # Update move-frequency mappings
            with open(unique_moves_file,'w') as file:
                for move,freq in move_frequencies.items():
                    file.write(f'{move}:{freq}\n')
            min_dissonance = dissonance
            break
        else:
            # Assign frequencies randomly to unique moves
            move_frequencies = assign_random_freq(unique_moves,freq_mat)
            run_count += 1
    print(f'Game {game_number+1} analysed..')
