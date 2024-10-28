import numpy as np
import pandas as pd
import os
import itertools
import json
import tqdm

def load_process_simulations(path): 
    simulations = np.load(path)
    def int_to_bit(n):
        binary = bin(n)[2:] 
        return binary.zfill(52)
    binary_decks = [int_to_bit(deck) for deck, seed in simulations]
    
    return binary_decks
#binary decks is a list of all decks as strings? 

    

def score_deck(deck: str,
               seq1: str,
               seq2: str) -> tuple[int]:
    '''
    Given a shuffled deck of cards, a sequence chosen by player1, and a sequence chosen by player two, 
    return the number of cards/tricks for each variation of Penney's Game.
    
    deck: randomnly shuffled deck of 52 cards
    seq1: the 3-card sequence chosen by player 1 (ex. BBB, RBR)
    seq2: the 3-card sequence chosen by player 2 (ex. RRR, BRB)
    '''
    p1_cards = 0
    p2_cards = 0
    pile = 2
    
    p1_tricks = 0
    p2_tricks = 0
    
    i = 0
    while i < len(deck) - 2:
        pile += 1
        current_sequence = deck[i:i+3]
        if current_sequence == seq1:
            p1_cards += pile
            pile = 2
            p1_tricks += 1
            i += 3
        elif current_sequence == seq2:
            p2_cards += pile
            pile = 2 
            p2_tricks += 1
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

        # if p2 wins set winner to 1, otherwise it is 0 (including draws).
        # if there is a draw, set draw counter to 1
        if p1_cards > p2_cards:
            cards_winner = 1
        elif p1_cards == p2_cards:
            cards_draw = 1
        if p1_tricks > p2_tricks:
            tricks_winner = 1
        elif p1_tricks == p2_tricks:
            tricks_draw = 1
        return cards_winner, cards_draw, tricks_winner, tricks_draw


def play_one_deck(deck: str, n: int, folder='results'):
    '''The function takes the deck string as an input and the file path to the results folder.
    The function plays out games between two players using all possible combinations of their strategies for a given
     deck of cards, calculates the outcomes (wins and draws), and saves the results in a specified directory.
     Saved in json file.'''

    sequences = ['000', '001', '010', '011', '100', '101', '110', '111']
    combinations = itertools.product(sequences, repeat=2)
    
    p1_wins_cards = {}
    p1_wins_tricks = {}
    draws_cards = {}
    draws_tricks = {}
    
    # Loop over all combinations of sequences
    for seq1, seq2 in combinations:
        p1_cards, p2_cards, p1_tricks, p2_tricks = score_deck(deck, seq1, seq2)
        cards, cards_tie, tricks, tricks_tie = calculate_winner(p1_cards, p2_cards, p1_tricks, p2_tricks)
        
        # Save the results for the current combination of sequences
        p1_wins_cards[(seq1, seq2)] = cards
        p1_wins_tricks[(seq1, seq2)] = tricks
        draws_cards[(seq1, seq2)] = cards_tie
        draws_tricks[(seq1, seq2)] = tricks_tie

    return cards, tricks, cards_tie, tricks_tie


def play_all_decks(path):
    simulations = np.load(path)
    def int_to_bit(n):
        binary = bin(n)[2:] 
        return binary.zfill(52)
    game_count = 0
    for deck, seed in simulations: #goes through all simulations and converts decks to bit 
        game_count += 1
        string_deck = int_to_bit(deck)

    # Prepare the data to save as a JSON file
    deck_data = {
        'cards': p1_wins_cards,
        'tricks': p1_wins_tricks,
        'card_ties': draws_cards,
        'trick_ties': draws_tricks,
        'n': n  # Save the total number of decks generated
    }

    json_file_path = os.path.join(folder, 'results.json')

    with open(json_file_path, 'w') as f:
        json.dump(deck_data, f)



# def sum_games(folder: str, average: bool):
#     '''Take all of the arrays in the specified folder, and add them together/divide by number of files to get the average 
#     if we are looking at win/loss (boolean is True). We don't find the average if we are looking at draws as we just want 
#       count how many ties there are (boolean is False) '''
#     files = [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))] # iterate through /data directory, only process files
#     games_total = None # where the sum of the games is going
#     for file in files:
#         file_path = os.path.join(folder,file) # get file name and directory
#         game = np.load(file_path, allow_pickle=True) # load the file
#         if games_total is None:
#             games_total = game # initialize games_total sum array
#         else:
#             games_total += game
#     num_games = len(files)
#     if average:
#         return np.divide(games_total, num_games)
#     return games_total # divide each individual element by the number of games played




# Functions for testing

# def shuffle_deck(seed:None):
#     '''Generates a single shuffled deck'''
#     rng = np.random.default_rng(seed = seed)
#     deck = np.ndarray.flatten((np.stack((np.ones(26), np.zeros(26)), axis= 0).astype(int)))
#     rng.shuffle(deck)
#     return ''.join(map(str, deck))

def play_n_games(n, data):
    for i in range(n):
        deck = shuffle_deck(i)
        play_one_deck(data = 'data/', deck = deck)

    filename = ['cards_win/', 'cards_draw/', 'tricks_win/', 'tricks_draw/']
    results = {}

    for folder in filename:
        if folder == 'cards_win/' or folder == 'tricks_win/':
            results[folder] = sum_games(f'{data}{folder}', True)
        elif folder == 'cards_draw/' or folder == 'tricks_draw/':
            results[folder] = sum_games(f'{data}{folder}', False)
    return results