import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px


def __make_annots(wins:np.ndarray, ties:np.ndarray):
    '''
    Generate annotations for heatmap values.
    Annot format: Win(Tie)
    '''
    annots = []
    for i in range(8):
        row = []
        for j in range(8):
            if np.isnan(wins[i,j]):
                row.append('')
            else:
                row.append(f'{str(int(wins[i,j]))} ({str(int(ties[i,j]))})')
        annots.append(row)
    return np.array(annots)

def __prepare_html(wins:np.ndarray, ties:np.ndarray, title:str) -> go.Figure :
    '''
    Returns a plotly heatmap.
    '''
    # Settings
    TITLE_SIZE = 22
    LABEL_SIZE = 18
    TICK_LABEL_SIZE = 16
    
    seqs = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']

    annots = __make_annots(wins, ties)
    fig = go.Figure(go.Heatmap(z=wins, x=seqs, y=seqs[::-1],
                               text=annots, texttemplate='%{text}', textfont={'size':15},
                               hovertemplate='Me: %{x}<br />Opponent: %{y}',
                               name='', # Remove trace in tooltip
                               colorscale='Blues', zmin=0, zmax=100,
                               colorbar=dict(ticksuffix='%')
                              ),
                   layout=go.Layout(plot_bgcolor='lightgray'))
    fig.update_layout(width=750, height=750, 
                      title=title, title_font_size=TITLE_SIZE,
                      title_x=0.5, title_y=0.92,
                      xaxis=dict(title='Me', title_font=dict(size=LABEL_SIZE), tickfont=dict(size=TICK_LABEL_SIZE)), 
                      yaxis=dict(title='Opponent', title_font=dict(size=LABEL_SIZE), tickfont=dict(size=TICK_LABEL_SIZE)))
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_traces(xgap=1, ygap=1, textfont_size=13)
    fig['layout']['yaxis']['autorange'] = 'reversed'
    return fig

def __create_seaborn(data:np.ndarray, annots:np.ndarray,
                     ax:plt.Axes = None, hide_yticks:bool = False, title:str = None
                    ) -> [plt.Figure, plt.Axes]:
    '''
    Returns a Seaborn heatmap.
    If ax is None, create a new figure. Otherwise, add the heatmap to the provided ax.
    '''
    seqs = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
    
    settings = {
        'vmin': 0,
        'vmax': 100,
        'linewidth': 0.01,
        'cmap': 'Blues',
        'cbar': False,
        'annot': annots,
        'fmt': ''
    }
    TICKLABEL_SIZE = 12
    TITLE_SIZE = 18
    
    if ax is None:
        # Create a new figure
        fig, ax = plt.subplots(1, 1, figsize=(16, 8))
    else:
        # Get the parent figure
        fig = ax.get_figure()

    sns.heatmap(data=data, ax=ax, **settings)

    ax.set_xticklabels(seqs, fontsize=TICKLABEL_SIZE)
    ax.set_yticklabels(seqs[::-1], fontsize=TICKLABEL_SIZE)
    ax.set_title(title, fontsize=TITLE_SIZE)
    ax.set_facecolor('lightgray')
    
    if hide_yticks:
        ax.set_yticks([])
    
    return fig, ax

    
def get_heatmaps(format:str = "html", results_path:str = "results/results.json") -> None:
    '''
    Produces two heatmaps using the data in the results folder.

    Args:
        format: Takes 'html' or 'png' as input. Determines file format of the saved heatmap.
        results_path: Defaults to results/results.json. Path to the results file to make heatmaps with.
    
    Returns:
        None: Saves the heatmap in the specified format.
    '''
    # Get data
    with open(results_path) as json_file:
        data = json.load(json_file)
    
    cards = np.array(data['cards']) * 100
    cards_ties = np.array(data['cards_ties']) * 100
    tricks = np.array(data['tricks']) * 100
    tricks_ties = np.array(data['tricks_ties']) * 100
    n = data['n']
        
    if format == 'html':
        # Variation 1
        cards_fig = __prepare_html(cards, cards_ties, title=f'My Chance of Winning by Cards<br />(from {n} Random Decks) [Win(Tie)]')
        path = '../figures/cards.html'
        cards_fig.write_html(path)
        print(f'{path} saved successfully.')
        cards_fig.show()
        
        # Variation 2
        tricks_fig = __prepare_html(cards, cards_ties, title=f'My Chance of Winning by Tricks<br />(from {n} Random Decks) [Win(Tie)]')
        path = '../figures/tricks.html'
        tricks_fig.write_html(path)
        print(f'{path} saved successfully.')
        tricks_fig.show()
    
    elif format == 'png':
        # Figure specifications
        LABEL_SIZE = 14
        TICK_SIZE = 10
        ANNOT_SIZE = 8
        
        fig, ax = plt.subplots(1, 2, 
                               figsize=(16,8), 
                               gridspec_kw={'wspace':.05})
    
        # Left heatmap
        cards_annots = __make_annots(cards, cards_ties)
        __create_seaborn(cards, cards_annots, ax[0], 
                         title=f'My Chance of Winning by Cards\n(from {n} Random Decks)')
        ax[0].set_xlabel('Me', fontsize=LABEL_SIZE)
        ax[0].set_ylabel('Opponent', fontsize=LABEL_SIZE)
    
        # Right heatmap
        tricks_annots = __make_annots(tricks, tricks_ties)
        __create_seaborn(tricks, tricks_annots, ax[1], 
                         title=f'My Chance of Winning by Tricks\n(from {n} Random Decks)',
                         hide_yticks=True)
        ax[1].set_xlabel('Me', fontsize=LABEL_SIZE)
    
        # Add custom colorbar
        cbar_ax = fig.add_axes([.92, 0.11, 0.02, .77])
        cb = fig.colorbar(ax[1].collections[0], cax=cbar_ax, format='%.0f%%')
        cb.outline.set_linewidth(.2)
        
        # Add caption
        fig.suptitle('Cell text are formatted as follows: Chance of Win (Chance of Tie)', x=0.3, y=0.01)
        fig.savefig('../figures/heatmaps.png')
    return
