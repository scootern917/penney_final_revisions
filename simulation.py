import numpy as np
import os
from IPython.display import clear_output

def generate_sequence(seed: int, seq: list) -> str:
    '''Takes unshuffled deck as input and outputs string version of shuffled deck.''' 
    
    np.random.seed(seed)
    np.random.shuffle(seq)
    return ''.join(map(str,seq))

#need to run with 1,000,000 iterations
def generate_data(n):
    '''Takes in number of simulations to be run, and shuffles deck n times'''

    if(os.path.exists("deck_data.npy")):
        deck_data = np.load("deck_data.npy", allow_pickle = True)
    else:
        deck_data = np.zeros((0, 2))
    seed = deck_data.shape[0]
    sequence = [1] * 26 + [0] * 26
    for x in (range(n)):
        np.random.seed(seed)
        shuffled_deck = generate_sequence(seed, sequence)
        new_row = np.array([seed, shuffled_deck], dtype=object)
        deck_data = np.vstack([deck_data, new_row])
        seed+=1
        if x%10000 == 0:
            clear_output()
            print(x)
    np.save("deck_data.npy", deck_data)
