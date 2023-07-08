# test the frequency-moveset generated from training
import chess
from chess import pgn
import numpy as np
import pygame
from scipy.signal import lfilter

# filters and effects
def sdelay(R,x):
    L = x.shape[0]
    b = np.sinc(np.arange(L) - R)
    y = lfilter(b,[1],x)
    return y

def reverb(R,alpha,x):
    b=np.hstack([alpha,np.zeros(R-2),1])
    a=np.hstack([1,np.zeros(R-2),alpha])
    y = lfilter(b,a,x)
    return y

def guitar_filt(freq,Fs,x):
    delay = int(Fs/freq+0.5)
    decay=0.1
    a = np.hstack([1,np.zeros(delay-3),-decay,decay-1])
    y = lfilter([1],a,x)
    return y

# create tone based on frequency
def create_detuned_pulse(freq, dur, Fs, A, num_oscillators, minor):
    # Generate multiple detuned pulse wave oscillators
    if num_oscillators==2:
        detune_factor = [1,3/2]
    elif num_oscillators==3:
        detune_factor = [1,5/4*(1-minor) + 6/5*minor,3/2]
    elif num_oscillators==4:
        detune_factor = [1,5/4*(1-minor) + 6/5*minor,3/2,15/8*(1-minor) + 7/4*minor]
    else:
        detune_factor = [1]
    
    offset=40                          # offset in milliseconds
    tones = np.array([])
    for i in range(num_oscillators):
        detuned_freq = freq*detune_factor[i]                            # Generate harmonics
        
        # Generate pulse wave oscillator
        samples = int(Fs / detuned_freq)
        cycles = int(detuned_freq*dur/1000)
        #pulse_table = A/num_oscillators*(np.hstack((np.ones(samples//2), -1*np.ones(samples//2))))
        #triagTable = A/num_oscillators*np.hstack((np.linspace(1,-1,int(samples/2)),np.linspace(-1,1,int(samples/2))))
        #randTable = A/num_oscillators*np.random.randn(samples)
        impulse = A/num_oscillators*np.hstack([1,np.zeros(samples*cycles-1)])
        
        # turn into guitar sound
        #pulse = guitar_filt(detuned_freq,samples,np.tile(triagTable, cycles))
        pulse = guitar_filt(detuned_freq,Fs,impulse)
        #pulse = np.tile(triagTable, cycles)
        
        # add reverb
        pulse = reverb(2,0.9,pulse)
        
        # add delay
        pulse = sdelay(Fs/offset*i,pulse)
        
        # combine
        tones = np.hstack((tones,pulse))
    
    # Combine the detuned oscillators
    #tone = np.zeros(np.max([i.shape for i in tones]))
    #for i in range(num_oscillators):
        #tone[:tones[i].shape[0]] += tones[i]
    
    return tones

# Create tune based on passed frequencies
def create_tune(freq_mat,Fs):
    dur=250
    tune=[]
    tone_dur = np.zeros(len(freq_mat))
    for ind,tune_freq in enumerate(freq_mat):
        note = create_detuned_pulse(freq=tune_freq, dur=dur, Fs=Fs, A=1, num_oscillators=3, minor=0)
        # Overlap the note with the previous note using crossfade
        if ind > 0:
            crossfade_samples = int(0.03 * Fs)  # Length of the crossfade region (10% of note duration)
            tune[-crossfade_samples:] *= np.linspace(1.0, 0.0, crossfade_samples)  # Fade out the end of the previous note
            note[:crossfade_samples] *= np.linspace(0.0, 1.0, crossfade_samples)  # Fade in the beginning of the current note
        tune = np.concatenate((tune, note))
        tone_dur[ind] = note.shape[0]/Fs*1000
    return tune,tone_dur

# create playable sound object
def create_sound(tune,Fs):
    pygame.init()
    pygame.mixer.init(frequency=Fs, size=-16, channels=2, buffer=4096)
    tnote = np.outer(tune, [1, 1])
    tnote = tnote * 32767 / np.max(np.abs(tnote))
    tnote = tnote.astype(np.int16)
    sound = pygame.sndarray.make_sound(tnote)
    return sound

Fs=44100
# open game and detect moves
pgn_test = open('./pgn_files/chess_game5.pgn', encoding='utf-8')
game = pgn.read_game(pgn_test)
board = game.board()
moves = list(game.mainline_moves())
pgn_moves = []
for ind,move in enumerate(moves):
    san_move = board.san(move)
    pgn_moves.append(san_move)
    board.push(move)

# read unique moves from file
move_freq_dict={}
with open('unique_moves.txt','r') as file:
    for line in file:
        move,freq = line.strip().split(':')
        move_freq_dict[move] = float(freq)

freq_moves = [move_freq_dict[key] for key in pgn_moves]
tune,tune_dur = create_tune(freq_moves,Fs)
sound = create_sound(tune,Fs)
if sound is not None:
    print('playing audio...')
    sound.play()
    pygame.time.wait(int(np.sum(tune_dur)))  # Delay to allow sound to play



