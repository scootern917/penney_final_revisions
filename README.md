# Project Penney

## Overview
Penney's Game is a competitive, probability-based game typically played between two players who select distinct three-card sequences (combinations of Red or Black). As cards are drawn, the first appearance of one of the selected sequences determines the winner of that round. There are two main variations of the game:

The **first variation** tallies the **total number of cards** from the initial draw until a chosen sequence appears. All cards in the pile are given to the player whose sequence appears. This is repeated until the deck runs out; any cards remaining in the pile at the end are not tallied.

The **second variation** counts the **number of "tricks" a player scores** in a game. Each time a player's sequence appears, their number of tricks increases by 1, repeated until the deck runs out.

Below, you may read the documentation on how our group approached simulating the game, managing/storing our data, and visualizing our data as a heatmap. The project includes # files:

- `simulation.py`
- `processing.py`
- `visualization.py`
- `runeverything.ipynb`

For more background, check out these resources:
- Penney's Game Wikipedia Page: https://en.wikipedia.org/wiki/Penney%27s_game
- Humble Nishiyama's Paper: https://www.datascienceassn.org/sites/default/files/Humble-Nishiyama%20Randomness%20Game%20-%20A%20New%20Variation%20on%20Penney%27s%20Coin%20Game.pdf
- Fun Video on Penney's Game: https://www.youtube.com/watch?v=s4tyO4V2im8

## Getting Started
Before running this project yourself, you can first start by familiarizing yourself with the files below or running the [run_all file](./run_all.ipynb). In this file you should start by running the simulation script and generating the necessary data for the later processing and visualization parts.  

## Simulation.py

`generate_sequence(seed: int, seq: list) -> str:`

Parameters:

- `seed` : random seed number used to shuffle the sequence
- `seq` : sequence to be shuffled

Returns:

- `str`: shuffled sequence as a string


`generate_data(n: int) -> None:`

Parameters:

- `n` : number of simulations to be created

Returns: `None`

Functionality:
- Creates decks of red and black cards, represented by 52 bits, where `0` is black and `1` is red. Each deck has a different has a different seed. 
- The 52 bits are shuffled, to represent a random deck with 26 black and 26 red cards.
- The decks and their seeds are saved as a 2D array into an `.npy` file 


---

## Processing.py

The Processing file has several functions associated with storing and processing data for visualization.

`load_decks(path: str) -> numpy.ndarray:`

Parameter:

- `path` (`str`): the location of the simulation data .npy file

Returns: 

- Array of simulations

Functionality:

- Loads simulation data from specified file
- Isolates decks from seeds 

`score_deck(score_deck(deck, seq1, seq2, deck_length)`

Parameters:
- `deck`: Deck of cards 
- `seq1`: 3-bit sequence for player 1
- `seq2`: 3-bit sequence for player 2
- `deck_length`: Length of deck to process (minus 2) 

Returns:
- Tuple containing the number of cards and tricks won by each player 

Functionality:
- Initialize card counts and pile size
- Iterates through the deck to check for matches with player sequences
- If match is found, matching player receives cards in pile and their trick count is updated

`calculate_winner(p1_cards, p2_cards, p1_tricks, p2_tricks) -> tuple[int, int, int, int]`

Parameter:
- `p1_cards`: number of cards from player 1
- `p2_cards`: number of cards from player 2
- `p1_tricks`: number of tricks from player 1
- `p2_tricks`: number of tricks from player 2

Returns:
- Tuple containing:
- `cards_winner`: 1 if player 1 won cards, 0 otherwise
- `cards_draw`: 1 if cards are tied, 0 otherwise
- `tricks_winner`: 1 if player 1 won tricks, 0 otherwise
- `tricks_draw`: 1 if tricks are tied, 0 otherwise

Functionality:
- Compares card and trick counts between players to determine who won based on tricks, cards, and/or if there is a tie 


`process_deck_batch(deck, valid_pairs, deck_length_minus2) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]`

Parameters:
- `deck` : Binary sequence representing the deck
- `valid_pairs` : List of valid sequence pairs to test
- `deck_length_minus2` : Deck length minus 2 for optimization


Returns:

- Tuple containing numpy arrays for card wins, trick wins, card ties, and trick ties of that batch
  
Functionality:
- Initializes four 8X8 zero matrices
- For each sequence pair it converts the sequence to their corresponding indices, calls score_deck and caculate_winner to get game outcomes and determine win/tie status, updates the corresponding matrices based on results 


`process_all_decks(decks, deck_length=52) -> dict`


Parameters:
- `decks`: List of decks to process
- `deck_length`: Length of deck (default 52)

Returns:

- Dictionary containing the 8X8 matrices for car win, trick win, card ties, and trick ties probabilities as well as the total number of decks processed 

Functionality:
- Initializes four 8X8 zero matrices for results
- For each deck in the input it calls process deck batch to get results for this deck, and adds the results in the corresponding matricies
- Converts raw counts to probabilities
- Converts numpy arrays to JSON

  `process_and_save_results(input_path, output_folder='results') -> dict`


Parameters:
- `input_path`: Path to input.npy file
- `output_folder`: Folder to save results (default: results) 

Returns:

- Dictionary containing processed results in the same format as `process_all_decks`

Functionality:
- Creates output folder if it doesn't exist
- Loads deck data from specified .npy file
- Processes all decks
- Saves results to json file named `results.json` in output folder



---

## Visualization.py


The Visualization file helps with generating and saving heatmaps for the probability of player 1 winning for every possible combination of color card sequences.

Note that the **title of the heatmaps contains an approximation** of the amount of games played. This number is taken from one of the variations. It is approximate because ties are dropped from the data, meaning that each game variation may have slightly different amounts of actual finished, non-tying games.

`get_heatmaps(format: str) -> None:`

Parameters:

- `format`: Takes 'html' or 'png' as input. Determines file format of the saved heatmap

Returns:

- `None`

Functionality:
- Saves a png or two html files that show heatmap visualizations of the simulation results.
- Both options include two heatmaps, one for each game variation.

---

## run_all.ipynb
This notebook allows you to run the entire process in sequence. Simply execute the notebook to:

Add new simulations.
Process the results.
Visualize the data through heatmaps.

---

## Files/Folders Included

`data/`: This directory contains the raw data generated by the simulations, stored in binary format (.npy). Note: for this project, the data may exceed GitHub's file size limits, so you may want to add this directory to .gitignore to avoid pushing large files to the repository. If skipped, create a placeholder file here called files_too_large.

`figures/`: Contains pre-generated visualizations of the simulation results in .html and .png formats. These figures provide a visual analysis of player win probabilities across sequence combinations and game variations.

`src/`: This directory contains all code files, including the simulation, data processing, and visualization scripts. The code is well-documented with type hints, docstrings, and comments for easy understanding and debugging.

`results/`: This directory contains a single file, results.json, summarizing the outcomes of simulations, such as win probabilities for each possible sequence combination across game variations. The results file consolidates data from multiple runs, showing statistical trends.

---

## Details

### Random Data Generation
The generate_data(n) function in Simulation.py generates n simulated decks of cards. Here’s how it works:

Deck Composition: Each deck declared consists of 52 cards (26 red and 26 black), represented as a binary sequence of 52 bits, where 1 represents a red card and 0 represents a black card.

Randomization: Each deck is assigned a unique random seed. The function shuffles the bits to simulate a randomized card sequence and stores each deck’s sequence and its seed as binary data.

Data Storage: The generated deck sequences are saved as .npy files in the data/ directory, ensuring that each deck's structure is reproducible based on its seed. This approach allows users to load the same dataset in the future and analyze or visualize consistent results.

Scoring Simulations
Once data is generated, it is processed in Processing.py to score each player based on their chosen sequences. Here’s an overview of each scoring variation:

**Variation 1** - Total Card Count:
The game iterates through the deck, comparing the drawn cards to the players’ selected sequences. When a player’s sequence appears, that player collects all cards drawn so far.

The process repeats until the deck runs out, and the player who accumulates the most cards wins.

Complexity: Since we iterate through the deck and check each sequence, this is approximately an O(n) operation per deck. Here, n represents the number of cards in the deck.

**Variation 2** - Trick Count:
Each time a player’s sequence appears, that player scores one trick, without collecting cards. The game continues until the deck is exhausted, and the player with the most tricks wins.

Complexity: This process is also O(n) per deck since we iterate once through the deck and check sequences along the way.

Assumptions and Symmetry:
Symmetry is assumed when comparing different sequences in the deck. This symmetry simplifies the computation by assuming that sequences such as ‘RBR’ and ‘BRB’ have equivalent likelihoods in opposite positions.

Analyzing Combinations:
The process_all_decks function tests every possible combination of player sequences to calculate winning percentages across variations. The results are saved as DataFrames for later analysis and visualization.

Results Presentation:
The simulation results are presented through heatmaps created in Visualization.py. Each heatmap shows the win probability for Player 1 across all sequence combinations:

### Figure Format: 
The visualizations for Project Penney are based on player win probabilities and tie counts, presented as heatmaps. These visualizations are created using the data stored in results/results.json, which contains five key elements:

'cards': Win probabilities by cards

'tricks': Win probabilities by tricks

'cards_ties': Number of ties by cards

'tricks_ties': Number of ties by tricks

'n': Total number of decks generated (sample size)

### Visualization Inputs


The heatmaps are generated from 8x8 arrays representing all combinations of Player 1 and Player 2's sequences. Each heatmap corresponds to one of the variations (cards or tricks) and shows the probabilities for Player 1 to win.

### Card Encoding and Matrix Layout

Card encoding:
- Black (B) = 0
- Red (R) = 1
- Matrix origin: (0,0) is located at the bottom-left corner of the heatmap.

Axes:
- X-axis: My sequence (Player 1)
- Y-axis: Opponent’s sequence (Player 2)

Labels and Titles:

- X-axis label: My sequence (Player 1)
- Y-axis label: Opponent’s sequence (Player 2)

Title:

For each variation (cards or tricks), the title of the heatmap will reflect the nature of the game, for example: "My Chance of Winning (By Cards)" or "My Chance of Winning (By Tricks)."

### Plotting Details

Heatmap library: The heatmaps are generated using Seaborn's heatmap function.
Colormap: The "Blues" colormap is used for better visual differentiation.
Figure Sizing and Font Details

Figure size: Sized so that two figures fit side-by-side on a standard 16:9 slide for easy presentation.

Font sizes:
- Title: Appropriately large to stand out.
- Numbers inside the heatmap: Displayed as whole numbers in the Win(Tie) format.
- X and Y labels: Adjusted for readability, with clear tick sizes.
- Diagonal: The diagonal of the heatmap is grayed out and does not show any numbers since players cannot have the same sequence. This distinction is made to ensure that the heatmaps only reflect unique competitions.

### Results Format

- Win/Tie Format: The results within the heatmap are displayed as whole numbers in the format of Win(Tie), which visually represents both the win percentages and ties for each sequence pair.

- These specifications are stored in a dictionary to maintain consistency and accuracy across all visualizations.







