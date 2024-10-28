"""module to extract some statistics"""
import pandas as pd
import numpy as np

# based on
# https://snippets.openvolley.org/indicators-and-statistics.html

def exsideoutrate(plays):
    """
    Calculate the expected sideout rate for reception plays.

    This function filters the reception plays, groups them by evaluation,
    and calculates the expected sideout rate, which is the average of the
    plays where the point was won by the receiving team.

    Args:
        plays (DataFrame): A DataFrame containing the plays, 
        with columns 'skill', 'evaluation', 'point_won_by', and 'team'.

    Returns:
        DataFrame: A DataFrame with the evaluation and the expected sideout rate.
    """
    lso = plays.loc[plays['skill'] == "Reception"]\
        .groupby('evaluation')\
        .apply(lambda x: pd.Series({'expected_sideout_rate':\
            (x['point_won_by'] == x['team']).mean()}))\
        .reset_index()
    return lso

def exsideoutratebyplayer(plays):
    """
    Calculate the expected sideout rate for each player based on reception plays.

    This function filters the reception plays, groups them by evaluation,
    and calculates the expected sideout rate. It then merges this information 
    back with the original plays and groups the result by player to calculate
    the number of receptions and the average expected sideout rate per player.

    Args:
        plays (DataFrame): A DataFrame containing the plays,
        with columns 'skill', 'evaluation', 'point_won_by', 'team', 'player_id', and 'player_name'.

    Returns:
        DataFrame: A DataFrame with each player's ID, name, number of receptions,
        and average expected sideout rate.
    """
    lso = plays.loc[plays['skill'] == "Reception"]\
        .groupby('evaluation')\
        .apply(lambda x: pd.Series({'expected_sideout_rate':\
            (x['point_won_by'] == x['team']).mean()}))\
        .reset_index()
    merged_plays = pd.merge(plays.loc[plays['skill']\
        == "Reception"], lso, on="evaluation", how="left")
    result = merged_plays.groupby(['player_id', 'player_name'])\
        .agg(n_receptions=('evaluation', 'size'),
            expected_sideout_rate=('expected_sideout_rate', 'mean'))\
        .reset_index()
    return result

def exbreakpointrate(plays):
    """
    Calculate the expected breakpoint rate for serve plays.

    This function filters the serve plays, groups them by evaluation,
    and calculates the expected breakpoint rate. The breakpoint rate is
    defined as the average of the plays where the point was won by the serving team.

    Args:
        plays (DataFrame): A DataFrame containing the plays,
        with columns 'skill', 'evaluation', 'point_won_by', and 'team'.

    Returns:
        DataFrame: A DataFrame with the evaluation and the expected breakpoint rate.
    """
    lbp = plays.loc[plays['skill'] == "Serve"]\
        .groupby('evaluation')\
        .agg(expected_breakpoint_rate=('team',\
            lambda x: x.eq(plays['point_won_by']).mean()))\
        .reset_index()
    return lbp

def exbreakpointratebyplayer(plays):
    """plays.loc[:, 'set_had_attack_kill'] = (plays['skill'] == "Set")
    Calculate the expected breakpoint rate for each player based on serve plays.

    This function filters the serve plays, groups them by evaluation,
    and calculates the expected breakpoint rate. It then merges this information 
    back with the original plays and groups the result by player to calculate
    the number of serves and the average expected breakpoint rate per player.

    Args:
        plays (DataFrame): A DataFrame containing the plays,
        with columns 'skill', 'evaluation', 'point_won_by', 'team', 'player_id', and 'player_name'.

    Returns:
        DataFrame: A DataFrame with each player's ID, name, number of serves,
        and average expected breakpoint rate.
    """
    lbp = plays.loc[plays['skill'] == "Serve"]\
        .groupby('evaluation')\
        .agg(expected_breakpoint_rate=('team',\
            lambda x: x.eq(plays['point_won_by']).mean()))\
        .reset_index()
    merged_plays = plays.loc[plays['skill'] == "Serve"]\
        .merge(lbp, on="evaluation", how="left")
    result = merged_plays.groupby(['player_id','player_name'])\
        .agg(n_serves=('evaluation', 'size'),
            expected_breakpoint_rate=('expected_breakpoint_rate', 'mean'))\
        .reset_index()
    return result

def setassistrate(plays):
    """
    Calculate the assist rate for sets followed by a winning attack by the same team.

    This function adds a new column to indicate whether a set was followed by a winning attack
    by the same team. It then filters the set plays and groups the result by team and attack phase
    to calculate the assist rate.

    Args:
        plays (DataFrame): A DataFrame containing the plays,
        with columns 'skill', 'evaluation', 'team', and 'attack_phase'.

    Returns:
        DataFrame: A DataFrame with each team's assist rate grouped by attack phase.
    """
    # Add a variable indicating whether a set
    # was followed by a winning attack by the same team
    plays = plays.copy()
    plays.loc[:, 'set_had_attack_kill'] = (plays['skill'] == "Set") &\
        (plays['skill'].shift(-1) == "Attack") & \
        (plays['evaluation'].shift(-1) == "Winning attack") & \
        (plays['team'].shift(-1) == plays['team'])

    # filter only the rows relative to the set
    set_rows = plays[plays['skill'] == "Set"]

    # Group by 'team' and 'phase' and calculate the support rate
    result = set_rows.groupby(['team', 'attack_phase']) \
        .agg(assist_rate=('set_had_attack_kill', lambda x: np.sum(x) / len(x))) \
        .reset_index()
    return result
