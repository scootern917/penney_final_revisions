import numpy as np
import os
from IPython.display import clear_output

def generate_sequence(seed: int, seq: list) -> str:
    '''Takes unshuffled deck as input and outputs string version of shuffled deck.''' 
    
    np.random.seed(seed)
    np.random.shuffle(seq)
    return ''.join(seq)

#need to run with 1,000,000 iterations
def generate_data(n):
    '''Takes in number of simulations to be run, and shuffles deck n times'''

    if (os.path.exists("deck_data.npy")):
        deck_data = np.load("deck_data.npy", allow_pickle = True)
        seeds = list(deck_data[0])
        decks = list(deck_data[1])
    else:
        seeds = []
        decks = []

    seed = len(seeds)
    sequence = ['1'] * 26 + ['0'] * 26
    for i in (range(n)):

        np.random.seed(seed)
        shuffled_deck = generate_sequence(seed, sequence)

        seeds += [seed]
        decks += [shuffled_deck]

        seed += 1

        if i%10000 == 0:
            clear_output()
            print(i)

    deck_data = np.array([seeds, decks])
    np.save("deck_data.npy", deck_data)
