import pandas as pd
import numpy as np
# Function to extract teams
def get_teams(rows_list):
    # Find the index of [3TEAMS]
    teams_index = rows_list.index('[3TEAMS]\n')
    # Extract home_team and visiting_team
    home_team = rows_list[teams_index + 1].strip()
    visiting_team = rows_list[teams_index + 2].strip()
    return home_team, visiting_team

# get player number out of code
def calculate_skill(row):
    if pd.isna(row['player_number']):
        return np.nan
    else:
        return row['code'][3]

skill_map = {
    "S": "Serve",
    "R": "Reception",
    "E": "Set", 
    "A": "Attack",
    "D": "Dig",
    "B": "Block",
    "F": "Freeball",
    "p": 'Point'
}

eval_codes = ["#", "+", '!', '-', '/', '=']