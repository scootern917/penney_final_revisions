import numpy as np
import itertools
import json
import os
from tqdm import tqdm

def load_decks(path):
    """Load deck data from .npy file and convert to binary strings."""
    data = np.load(path, allow_pickle = True)
    decks = data[:, 1]
    decks.tolist()
   
    decks = decks[:30000] #for testing making it shorter
    #TODO remove this line
    
    return decks

def score_deck(deck: str, seq1: str, seq2: str, deck_length: int) -> tuple[int, int, int, int]:
    """Score a single deck for both players."""
    p1_cards = p2_cards = 0
    p1_tricks = p2_tricks = 0
    pile = 2
    i = 0
    
    while i < deck_length:
        pile += 1
        current_sequence = deck[i:i+3]
        if current_sequence == seq1:
            p1_cards += pile
            p1_tricks += 1
            pile = 2
            i += 3
        elif current_sequence == seq2:
            p2_cards += pile
            p2_tricks += 1
            pile = 2
            i += 3
        else:
            i += 1
    
    return p1_cards, p2_cards, p1_tricks, p2_tricks

def calculate_winner(p1_cards: int,
                     p2_cards: int,
                     p1_tricks: int,
                     p2_tricks: int):

        '''Given the number of cards and tricks for each player, calculate who wins for cards and tricks, as well as draws for cards and tricks.
            If player one wins, the winner is set to 0. If player 2 wins, the winner is set to 1.
            Also indicates if there was a draw.

        Arguments:
            p1_cards (int): number of cards player 1 won
            p2_cards (int): number of cards player 2 won
            p1_tricks (int): number of tricks player 1 won
            p2_tricks (int): number of tricks player 2 won
        
        Output:
            cards_winner (int): specifies who won based on cards
            cards_draw (int): 1 if a draw occurred, 0 otherwise
            tricks_winner (int): specifies who won based on tricks
            tricks_draw (int): 1 if a draw occured, 0 otherwise'''
        cards_winner = 0
        cards_draw = 0
        tricks_winner = 0
        tricks_draw = 0

   
        if p1_cards > p2_cards:
            cards_winner = 1
        elif p1_cards == p2_cards:
            cards_draw = 1
        if p1_tricks > p2_tricks:
            tricks_winner = 1
        elif p1_tricks == p2_tricks:
            tricks_draw = 1
        return cards_winner, cards_draw, tricks_winner, tricks_draw


def generate_unique_combinations(sequences: list[str]) -> set[tuple[str, str]]:
    """
    Generate unique combinations from the given sequences, including inverted pairs.
    Lets us calculate just 16 instead of 28 (minus swapped pairs) or 56 (minus diagonal) or all 64.
    
    Inputs:
    - sequences (list of str): List of binary sequences to generate combinations from.
    Returns:
    - set: Set of unique sequence pairs (accounting for inversions).
    """
    # Step 1: Generate all unique pairs of sequences without repetition
    pairs = set(itertools.combinations(sequences, 2))
    
    # Step 2: Use a set to store unique combinations considering inversion
    unique_combinations = set()
    
    for pair in pairs:
        bin1, bin2 = pair
        
        # Create the inverted version of the pair
        inverted_pair = ('{0:03b}'.format(~int(bin1, 2) & 7), '{0:03b}'.format(~int(bin2, 2) & 7))
        
        # Sort both the pair and the inverted pair to standardize
        sorted_pair = tuple(sorted(pair))
        sorted_inverted_pair = tuple(sorted(inverted_pair))
        
        # Add the pair only if its inverse or its swapped version isn't already present
        if sorted_inverted_pair not in unique_combinations:
            unique_combinations.add(sorted_pair)
    
    return unique_combinations

def complete_matrices(partial_results, sequences):
    """
    Complete the matrices for player 1's perspective using the computed values.
    When the players are flipped (i.e. looking at the opposite side of the matrix),
    player 1's wins become 0 (losses) while ties remain the same.
    
    Args:
        partial_results (dict): Dictionary containing partially filled matrices
        sequences (list): List of all possible sequences
    
    Returns:
        dict: Dictionary containing completed matrices
    """
    n_sequences = len(sequences)
    
    # Create complete matrices
    complete_cards_wins = np.zeros((n_sequences, n_sequences))
    complete_tricks_wins = np.zeros((n_sequences, n_sequences))
    complete_cards_ties = np.zeros((n_sequences, n_sequences))
    complete_tricks_ties = np.zeros((n_sequences, n_sequences))
    
    # Fill in the matrices
    for i in range(n_sequences):
        for j in range(n_sequences):
            if i != j:  # Skip diagonal 
                if j > i:  # Upper triangle??? 
                    complete_cards_wins[i][j] = partial_results['cards'][i][j]
                    complete_tricks_wins[i][j] = partial_results['tricks'][i][j]
                    complete_cards_ties[i][j] = partial_results['cards_ties'][i][j]
                    complete_tricks_ties[i][j] = partial_results['tricks_ties'][i][j]
                else:  # Lower triangle??
                    # Win probability for seq2 vs seq1 is 1 - (win probability for seq1 vs seq2) - (tie probability)  IDK if this logic is correct
                    complete_cards_wins[i][j] = 1 - partial_results['cards'][j][i] - partial_results['cards_ties'][j][i]
                    complete_tricks_wins[i][j] = 1 - partial_results['tricks'][j][i] - partial_results['tricks_ties'][j][i]
                    # Ties 
                    complete_cards_ties[i][j] = partial_results['cards_ties'][j][i]
                    complete_tricks_ties[i][j] = partial_results['tricks_ties'][j][i]
    
    return {
        'cards': complete_cards_wins.tolist(),
        'tricks': complete_tricks_wins.tolist(),
        'cards_ties': complete_cards_ties.tolist(),
        'tricks_ties': complete_tricks_ties.tolist(),
        'n': partial_results['n']
    }

def process_all_decks(decks, deck_length = 52):
    """Process all decks and compute statistics for all sequence combinations."""
    sequences = ['000', '001', '010', '011', '100', '101', '110', '111']
    n_sequences = len(sequences)
    
    unique_combinations = generate_unique_combinations(sequences) #gives us 16 combos to use
    
    # Initialize result arrays
    cards_wins = np.zeros((n_sequences, n_sequences))
    tricks_wins = np.zeros((n_sequences, n_sequences))
    cards_ties = np.zeros((n_sequences, n_sequences))
    tricks_ties = np.zeros((n_sequences, n_sequences))
    
    # Create sequence index mapping
    seq_to_idx = {seq: idx for idx, seq in enumerate(sequences)}
    
    total_decks = len(decks)
    deck_length_minus2 = deck_length - 2
    
    # Process each deck
    # for deck in tqdm(decks, desc="Processing decks"):
    #     for seq1 in sequences: #using unique_combinations would generate half the gird, 28 pairs
    #         for seq2 in sequences: 
    #             if seq1 != seq2: 
    #                 idx1 = seq_to_idx[seq1]  # Getting index of sequence 1
    #                 idx2 = seq_to_idx[seq2]  # Getting index of sequence 2
                
    #                 p1_cards, p2_cards, p1_tricks, p2_tricks = score_deck(deck, seq1, seq2, deck_length_minus2)
    #                 cards_winner, cards_draw, tricks_winner, tricks_draw = calculate_winner(p1_cards, p2_cards, p1_tricks, p2_tricks)
    
            
    #                 if cards_draw:
    #                     cards_ties[idx1][idx2] += 1
    #                 elif cards_winner == 1:  # Player 1 wins
    #                     cards_wins[idx1][idx2] += 1
            
    #                 if tricks_draw:
    #                     tricks_ties[idx1][idx2] += 1
    #                 elif tricks_winner == 1:  # Player 1 wins
    #                     tricks_wins[idx1][idx2] += 1

    for deck in tqdm(decks, desc="Processing decks"):
        for seq1, seq2 in unique_combinations:
            if seq1 != seq2: 
                idx1 = seq_to_idx[seq1]  # Getting index of sequence 1
                idx2 = seq_to_idx[seq2]  # Getting index of sequence 2
                
                p1_cards, p2_cards, p1_tricks, p2_tricks = score_deck(deck, seq1, seq2, deck_length_minus2)
                cards_winner, cards_draw, tricks_winner, tricks_draw = calculate_winner(p1_cards, p2_cards, p1_tricks, p2_tricks)
    
            
                if cards_draw:
                     cards_ties[idx1][idx2] += 1
                elif cards_winner == 1:  # Player 1 wins
                    cards_wins[idx1][idx2] += 1
            
                if tricks_draw:
                    tricks_ties[idx1][idx2] += 1
                elif tricks_winner == 1:  # Player 1 wins
                    tricks_wins[idx1][idx2] += 1    
            

    # Convert to probabilities
    partial_results = {
        'cards': cards_wins / total_decks,
        'tricks': tricks_wins / total_decks,
        'cards_ties': cards_ties / total_decks,
        'tricks_ties': tricks_ties / total_decks,
        'n': total_decks
    }
    
    # Complete the matrices
    final_results = complete_matrices(partial_results, sequences)
    
    return final_results



def process_and_save_results(input_path, output_folder='results'):
    """Process decks from input file and save results to output folder."""
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Load and process decks
    print("Loading decks...")
    decks = load_decks(input_path)
    
    # Process all decks and get results
    print("Processing games...")
    results = process_all_decks(decks)
    
    # Save results
    output_path = os.path.join(output_folder, 'results.json')
    with open(output_path, 'w') as f:
        json.dump(results, f)
    
    return results

# Example usage
# process_and_save_results("path_to_your_npy_file.npy")