"""module to filtering actions"""
import pandas as pd

# Filtering 
# Aim: find attacks after perfect or good reception
def filteringattack(plays):
    """
    Filters the plays DataFrame to include only attacking plays during the reception phase 
    with perfect or positive reception quality, and calculates the kill rate for each team.

    Parameters:
    plays (DataFrame): A pandas DataFrame containing play-by-play data.

    Returns:
    DataFrame: A pandas DataFrame with the kill rate for each team.
    """
    filtered_plays = plays[(plays['skill'] == 'Attack') &\
            (plays['point_phase'] == 'Reception') &\
            (plays['reception_quality'].str.contains('Perfect|Positive'))]
    result = filtered_plays.groupby('team')['evaluation'].\
        apply(lambda x: (x == 'Winning attack').mean()).reset_index(name='kill_rate')
    return(result)

#Aim: find rows corresponding to the first transition attack 
#opportunity in each rally (i.e. after the receiving team has attacked, find the first attack by the serving team).
def firsttransattack(plays):
    """
    Identifies the first transition attack opportunity 
    in each rally, i.e., the first attack by the serving team 
    after the receiving team has attacked.

    Parameters:
    plays (DataFrame): A pandas DataFrame containing play-by-play data.

    Returns:
    DataFrame: A pandas DataFrame with an additional column
    'is_fta' indicating if the row corresponds to the first 
    transition attack opportunity in each rally.

    The function performs the following steps:
    1. Filters the plays DataFrame to find the reception phase for each rally.
    2. Increments the possession number to identify the first transition attack.
    3. Merges this information back into the original plays DataFrame.
    4. Adds a column 'is_fta' to indicate the first transition attack.
    5. Prints the count of True and False values in the 'is_fta' column.

    Example:
    plays_with_fta = firsttransattack(plays)
    """
    reception_phase = \
        plays[plays['skill'] == "Reception"]\
        .groupby(['match_id', 'rally_number'])\
        .agg(possesion_number=('possesion_number', 'min')).reset_index()
    reception_phase['possesion_number'] += 1
    reception_phase['is_fta'] = True
    plays = pd.merge(plays, \
        reception_phase[['match_id', 'rally_number',\
        'possesion_number', 'is_fta']],\
        on=['match_id', 'rally_number', 'possesion_number'], how='left')
    plays['is_fta'] = plays['is_fta'].fillna(False)
    # Stampare il conteggio dei valori True e False nella colonna is_fta
    #print("Count of True values in is_fta:", plays['is_fta'].sum())
    #print("Count of False values in is_fta:", (~plays['is_fta']).sum())
    return plays