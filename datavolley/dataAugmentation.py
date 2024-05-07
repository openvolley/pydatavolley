import pandas as pd
from IPython.display import Markdown
import numpy as np



#Some examples of adding extra columns to our play-by-play data in order to support particular analyses, or to make other data-wrangling tasks easier.





# Aim: Identify the player who made the set associated with each attack (noting that some files might not have the setting action coded for all attacks, or even coded at all).

def setterOfAttackplays(plays):
    plays['set_player_name'] = np.where((plays['skill'] == 'Attack') & (plays['skill'].shift(1) == 'Set') & (plays['team'] == plays['team'].shift(1)), plays['player_name'].shift(1), np.nan)
    filtered_plays = plays[plays['skill'] == 'Attack'][['team', 'player_name', 'skill', 'evaluation_code', 'set_player_name']].head(5)


# Aim: identify the player_id of the setter on court for each data row.

def setPlayerId(plays):
    def assign_setter_id(row):
        if row['setter_position'] == 0:
            return None
        else:
            try:
                return row['home_p' + str(row['setter_position'])]
            except KeyError:
                return None

    plays['setter_id'] = plays.apply(assign_setter_id, axis=1)





# Aim: add a column that tells us the reception quality associated with each rally.

def receptionQuality(plays):
  
    reception_rows = plays[plays['skill'] == 'Reception']

    
    grouped_reception = reception_rows.groupby(['set_number', 'rally_number'])

    
    def calculate_reception_quality(group):
        if len(group) == 1:
            return group['evaluation'].iloc[0]
        else:
            return None

    
    rq = grouped_reception.apply(calculate_reception_quality).reset_index(name='reception_quality')

    plays = pd.merge(plays, rq, on=['set_number', 'rally_number'], how='left')

    return plays 

    
