"""module to enrich data"""
import pandas as pd
import numpy as np

# Some examples of adding extra columns to our play-by-play data in order 
#to support particular analyses, or to make other data-wrangling tasks easier.
# Aim:
# Identify the player who made the set associated with each attack 
# (nothing that some files might not have the setting action coded
# for all attacks, or even coded at all).

def setterofattackplays(plays):
    """
    This function identifies the setter 
    for each attack play in a volleyball match.

    It adds a new column 'set_player_name' to the DataFrame, 
    which contains the name of the player
    who performed the set immediately before the attack, 
    if the set and attack were made by the
    same team. If these conditions are not met, the value is set to NaN.

    Args:
    plays (DataFrame): 
    A pandas DataFrame containing volleyball play data, with at least the columns
        'skill', 'team', and 'player_name'.

    Returns:
    DataFrame: 
    A filtered DataFrame containing only the first 5 rows of attack plays, with columns
        'team', 'player_name', 'skill', 'evaluation_code', and 'set_player_name'.
    """
    plays['set_player_name'] = np.where((plays['skill'] == 'Attack') &
                                        (plays['skill'].shift(1) == 'Set') &
                                        (plays['team'] == plays['team'].shift(1)),
                                        plays['player_name'].shift(1), np.nan)
    filtered_plays = \
        plays[plays['skill'] == 'Attack']\
            [['team', 'player_name',\
               'skill', 'evaluation_code', 'set_player_name']].head(5)
    return filtered_plays

def setplayerid(plays):
    """
    Identifies the player_id of the setter on court for each data row.

    This function adds a new column 'setter_id' to the DataFrame, which contains the player_id
    of the setter based on the 'setter_position' value. If 'setter_position' is 0 or if there's 
    an issue accessing the player_id, the value is set to None.

    Args:
    plays (DataFrame): A pandas DataFrame containing volleyball play data with columns 
                       'setter_position' and 'home_pX' where X is a position number.

    Returns:
    DataFrame: The modified DataFrame with an additional column 'setter_id'.
    """
    def assign_setter_id(row):
        if row['setter_position'] == 0:
            return None
        try:
            return row['home_p' + str(row['setter_position'])]
        except KeyError:
            return None

    plays['setter_id'] = plays.apply(assign_setter_id, axis=1)
    return plays


def receptionquality(plays):
    """
    Adds a column that indicates the reception quality associated with each rally.

    This function identifies the reception quality for each rally based on the 'skill' column.
    It adds a new column 'reception_quality' to the DataFrame, which contains the evaluation of
    the reception if there is exactly one reception per rally. If there are multiple receptions
    or no receptions in a rally, the value is set to None.

    Args:
    plays (DataFrame): A pandas DataFrame containing volleyball play data with columns 'set_number',
                       'rally_number', 'skill', and 'evaluation'.

    Returns:
    DataFrame: The modified DataFrame with an additional column 'reception_quality'.
    """
    reception_rows = plays[plays['skill'] == 'Reception']
    grouped_reception = reception_rows.groupby(['set_number', 'rally_number'])
    
    def calculate_reception_quality(group):
        if len(group) == 1:
            return group['evaluation'].iloc[0]
        return None
    
    rq = grouped_reception.apply(calculate_reception_quality).reset_index(name='reception_quality')
    plays = pd.merge(plays, rq, on=['set_number', 'rally_number'], how='left')
    return plays
