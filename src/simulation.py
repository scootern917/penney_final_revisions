import numpy as np
from tqdm import tqdm
from typing import List
from datetime import datetime
import os

def generate_data(num_iterations: int) -> None:
    """
    Simulates shuffling a deck of red and black cards and saves the results.

    Parameters:
    - num_iterations: int, number of times to shuffle the deck and store the result.

    Returns:
    - None: Saves results to a .npy file instead of returning a list.
    """
    # Define the deck: 26 red cards (1s) and 26 black cards (0s)
    red = '1' * 26
    black = '0' * 26
    deck = black + red  # Deck is now a string of '0's and '1's

    # Initialize results array to store the seed and shuffled deck
    results = np.empty((num_iterations, 2), dtype=object)
    print(results.shape)
    
    for i in tqdm(range(num_iterations)):
        seed = i + 1  # Start seed at 1 and increment by 1 for each iteration
        shuffled_deck = generate_sequence(deck, seed)  # Shuffle the deck with the current seed
        results[i] = [seed, int(''.join(shuffled_deck), 2)]  # Store seed and shuffled deck as binary integer

    # Generate the filename with num_iterations and current date and time
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

    cwd = os.getcwd() # Current working directory
    filename = f"{cwd}/data/deck_data_{num_iterations}_{current_datetime}.npy"
    
    np.save(filename, results)  # Save the results array to a .npy file in the data subfolder

    print(f"{num_iterations} new decks saved to {filename}")


def generate_sequence(seq: str, seed: int) -> List[str]:
    """
    Generates a shuffled sequence (deck) based on a seed.

    Parameters:
    - seed: int, the seed for reproducibility.
    - seq: str, the string representing the deck of cards.

    Returns:
    - list: Shuffled deck as a list of characters.
    """
    np.random.seed(seed)  # Set the random seed for reproducibility
    seq_list = list(seq)  # Convert the string into a list of characters
    np.random.shuffle(seq_list)  # Shuffle the list in place
    return seq_list  # Return the shuffled deck as a list of characters

if __name__ == "__main__":
    # Generate 100,000 simulation results
    res = generate_data(1000000)
    print(res)
    print(res[-1])  # Print the last simulation result