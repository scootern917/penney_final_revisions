# Project Penney
"Alone we can do so little; together we can do so much." – Helen Keller

## Overview
Penney's Game is a competitive, probability-based game typically played between two players who select distinct three-card sequences (combinations of Red or Black). As cards are drawn, the first appearance of one of the selected sequences determines the winner of that round. There are two main variations of the game:

The **first variation** tallies the **total number of cards** from the initial draw until a chosen sequence appears. All cards in the pile are given to the player whose sequence appears. This is repeated until the deck runs out; any cards remaining in the pile at the end are not tallied.

The **second variation** counts the **number of "tricks" a player scores** in a game. Each time a player's sequence appears, their number of tricks increases by 1, repeated until the deck runs out.

Below, you may read the documentation on how our group approached simulating the game, managing/storing our data, and visualizing our data as a heatmap. The project includes # files:

- `Simulation.py`
- `Processing.py`
- `Visualization.py`
- `RunEverything.ipynb`

For more background, check out these resources:
- Penney's Game Wikipedia Page: https://en.wikipedia.org/wiki/Penney%27s_game
- Humble Nishiyama's Paper: https://www.datascienceassn.org/sites/default/files/Humble-Nishiyama%20Randomness%20Game%20-%20A%20New%20Variation%20on%20Penney%27s%20Coin%20Game.pdf
- Fun Video on Penney's Game: https://www.youtube.com/watch?v=s4tyO4V2im8

## Getting Started
Before running this project yourself, you can first start by familiarizing yourself with the files below or running the [run_all file](./run_all.ipynb). In this file you should start by running the simulation script and generating the necessary data for the later processing and visualization parts.  

## Simulation.py
The Simulation file will simulate the shuffling of decks of cards and save the results as a `.npy` file.

`generate_data(n)`

Parameters:
- `n` (`int`): number of simulations to be created

Functionality:
- Creates decks of red and black cards, represented by 52 bits, where `0` is black and `1` is red. Each deck has a different has a different seed. 
- The 52 bits are shuffled, to represent a random deck with 26 black and 26 red cards.
- The decks and their seeds are saved to an `npy` file 


---

## Processing.py
The Processing file has several functions associated with storing and processing data for visualization.

`load_process_simulations(path)`

Parameter:
- `path` (`str`): the location of the simulation data from the previous step

  
Functionality:
- Loads simulation data from specified file
- Converts each integer in file to 52-bit binary string
- Returns a list of the binary strings


`variation1`

Parameters:
- `deck` (`str`): deck of cards as binary sequence
- `player1_sequence` (`str`): 3-bit sequence for player 1
- `player2_sequence` (`str`): 3-bit sequence for player 2

Functionality:
- Initialize card counts and pile size
- Iterates through the deck to check for matches with player sequences
- If match is found, matching player receives cards in pile
- Returns `player1_cards, player2_cards`: the number of **cards** collected by each player

`variation2`

Parameters:
- `deck` (`str`): deck of cards as binary sequence
- `player1_sequence` (`str`): 3-bit sequence for player 1
- `player2_sequence` (`str`): 3-bit sequence for player 2

Functionality:
- Initialize trick counters for both players
- Iterates through deck to check for matches with player sequences
- When a match is found, matching player scores one trick
- Returns `player1_tricks, player2_tricks`: number of **tricks** won by each player


`analyze_all_combinations`

Parameter:
- `simulations`: list of binary strings representing games

Functionality:
- Generates all possible player 1 and player 2 sequence combinations 
- For each unique pair of sequences it simulations both variations of the game for each deck in simulations, counts wins for each player in both variations, and calculates win percentages
- Compiles results into two DataFrames, one for each variation


`combine_past_data`

Parameters:
- `new_var1` (`pandas.DataFrame`): New simulation data to be added to old data for variation 1.
- `new_var2` (`pandas.DataFrame`): New simulation data to be added to old data for variation 2.
- `var1_existing_filename` (`str`): The CSV file containing the old data for variation 1.
- `var2_existing_filename` (`str`): The CSV file containing the old data for variation 2.
- `folder` (`str`, optional): Path to the folder containing the CSV files to process. Default is `data`.

  
Functionality:
- Initializes combined DataFrames for each variation using existing data
- Sets ‘Sequence 1’ and ‘Sequence 2’ as index
- Reads CSVs, ensures sequences are 3 digits long, determines which variation the file belongs to, updates corresponding combined DataFrame using `update_dataframe` function
- Resets index of combined DataFrames
- Saves updated DataFrames to CSV files 
- Returns the two updated DataFrames 


`update_dataframe`


Parameters:
- `existing_df` (`pandas.DataFrame`): Existing DataFrame to be updated
- `new_df` (`pandas.DataFrame`): DataFrame containing data to be merged


Functionality:
- If the existing DataFrame is empty, it returns the new DataFrame
- Finds common columns between existing and new DataFrames
- Updates existing DataFrame with values from common columns in new DataFrame
- Recalculates the ‘Player 1 Win %’ based on updated win counts 
- Returns updated DataFrame with merged data and recalculated win percentages 



---

## Visualization.py


The Visualization file helps with generating and saving heatmaps for the probability of player 1 winning for every possible combination of color card sequences.

Note that the **title of the heatmaps contains an approximation** of the amount of games played. This number is taken from one of the variations. It is approximate because ties are dropped from the data, meaning that each game variation may have slightly different amounts of actual finished, non-tying games.

`get_heatmaps`

Parameters:
- `format`: Takes 'html' or 'png' as input. Determines file format of the saved heatmap

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

data/: This directory contains the raw data generated by the simulations, stored in binary format (.npy). Note: for this project, the data may exceed GitHub's file size limits, so you may want to add this directory to .gitignore to avoid pushing large files to the repository. If skipped, create a placeholder file here called files_too_large.
figures/: Contains pre-generated visualizations of the simulation results in .html and .png formats. These figures provide a visual analysis of player win probabilities across sequence combinations and game variations.
src/: This directory contains all code files, including the simulation, data processing, and visualization scripts. The code is well-documented with type hints, docstrings, and comments for easy understanding and debugging.
results/: This directory contains a single file, results.json, summarizing the outcomes of simulations, such as win probabilities for each possible sequence combination across game variations. The results file consolidates data from multiple runs, showing statistical trends.
