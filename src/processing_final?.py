import numpy as np
import itertools
import json
import os
from tqdm import tqdm

# Global constants
SEQUENCES = ['000', '001', '010', '011', '100', '101', '110', '111']
SEQ_TO_IDX = {seq: idx for idx, seq in enumerate(SEQUENCES)}
VALID_PAIRS = [(seq1, seq2) for seq1 in SEQUENCES for seq2 in SEQUENCES if seq1 != seq2]

def load_decks(path):
    """Load deck data from .npy file."""
    data = np.load(path, allow_pickle=True)
    return data[:, 1]

def score_deck(deck, seq1, seq2, deck_length):
    """Optimized scoring function."""
    p1_cards = p2_cards = 0
    p1_tricks = p2_tricks = 0
    pile = 2
    i = 0
    seq_len = 3
    
    while i < deck_length:
        pile += 1
        current = deck[i:i+seq_len]
        if current == seq1:
            p1_cards += pile
            p1_tricks += 1
            pile = 2
            i += seq_len
        elif current == seq2:
            p2_cards += pile
            p2_tricks += 1
            pile = 2
            i += seq_len
        else:
            i += 1
    
    return p1_cards, p2_cards, p1_tricks, p2_tricks

def calculate_winner(p1_cards, p2_cards, p1_tricks, p2_tricks):
    """Calculate winner status."""
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

def process_deck_batch(deck, valid_pairs, deck_length_minus2):
    """Process a single deck for all valid pairs."""
    n_sequences = len(SEQUENCES)
    batch_cards_wins = np.zeros((n_sequences, n_sequences))
    batch_tricks_wins = np.zeros((n_sequences, n_sequences))
    batch_cards_ties = np.zeros((n_sequences, n_sequences))
    batch_tricks_ties = np.zeros((n_sequences, n_sequences))
    
    for seq1, seq2 in valid_pairs:
        idx1 = SEQ_TO_IDX[seq1]
        idx2 = SEQ_TO_IDX[seq2]
        
        p1_cards, p2_cards, p1_tricks, p2_tricks = score_deck(deck, seq1, seq2, deck_length_minus2)
        cards_winner, cards_draw, tricks_winner, tricks_draw = calculate_winner(p1_cards, p2_cards, p1_tricks, p2_tricks)
        
        if cards_draw:
            batch_cards_ties[idx1][idx2] += 1
        elif cards_winner == 1:
            batch_cards_wins[idx1][idx2] += 1
        
        if tricks_draw:
            batch_tricks_ties[idx1][idx2] += 1
        elif tricks_winner == 1:
            batch_tricks_wins[idx1][idx2] += 1
            
    return batch_cards_wins, batch_tricks_wins, batch_cards_ties, batch_tricks_ties

def process_all_decks(decks, deck_length=52):
    """Process all decks with visible progress bar."""
    n_sequences = len(SEQUENCES)
    total_decks = len(decks)
    deck_length_minus2 = deck_length - 2
    
    # Initialize result arrays
    cards_wins = np.zeros((n_sequences, n_sequences))
    tricks_wins = np.zeros((n_sequences, n_sequences))
    cards_ties = np.zeros((n_sequences, n_sequences))
    tricks_ties = np.zeros((n_sequences, n_sequences))
    
    # Process each deck
    for deck in tqdm(decks, desc="Processing decks"):
        batch_cw, batch_tw, batch_ct, batch_tt = process_deck_batch(
            deck, VALID_PAIRS, deck_length_minus2)
        cards_wins += batch_cw
        tricks_wins += batch_tw
        cards_ties += batch_ct
        tricks_ties += batch_tt

    # Convert to probabilities and lists
    results = {
        'cards': (cards_wins / total_decks).tolist(),
        'tricks': (tricks_wins / total_decks).tolist(),
        'cards_ties': (cards_ties / total_decks).tolist(),
        'tricks_ties': (tricks_ties / total_decks).tolist(),
        'n': total_decks
    }
    
    return results

def process_and_save_results(input_path, output_folder='results'):
    """Process decks from input file and save results."""
    os.makedirs(output_folder, exist_ok=True)
    
    print("Loading decks...")
    decks = load_decks(input_path)
    
    print("Processing games...")
    results = process_all_decks(decks)
    
    output_path = os.path.join(output_folder, 'results.json')
    with open(output_path, 'w') as f:
        json.dump(results, f)
    
    return results