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

desired_order = [
    'match_id', 'point_id', 'video_file_number', 'video_time', 'code', 'team', 'player_number', 'player_name',
    'player_id', 'skill', 'skill_type', 'evaluation_code', 'evaluation', 'attack_code', 'attack_description',
    'set_code', 'set_description', 'set_type', 'start_zone', 'end_zone', 'end_subzone', 'end_cone', 'skill_subtype',
    'num_players', 'num_players_numeric', 'special_code', 'timeout', 'end_of_set', 'substitution', 'point',
    'home_team_score', 'visiting_team_score', 'home_setter_position', 'visiting_setter_position', 'custom_code',
    'file_line_number', 'home_p1', 'home_p2', 'home_p3', 'home_p4', 'home_p5', 'home_p6', 'visiting_p1', 'visiting_p2',
    'visiting_p3', 'visiting_p4', 'visiting_p5', 'visiting_p6', 'start_coordinate', 'mid_coordinate', 'end_coordinate',
    'point_phase', 'attack_phase', 'start_coordinate_x', 'start_coordinate_y', 'mid_coordinate_x', 'mid_coordinate_y',
    'end_coordinate_x', 'end_coordinate_y', 'home_player_id1', 'home_player_id2', 'home_player_id3', 'home_player_id4',
    'home_player_id5', 'home_player_id6', 'visiting_player_id1', 'visiting_player_id2', 'visiting_player_id3',
    'visiting_player_id4', 'visiting_player_id5', 'visiting_player_id6', 'set_number', 'team_touch_id', 'home_team',
    'visiting_team', 'home_team_id', 'visiting_team_id', 'team_id', 'point_won_by', 'winning_attack', 'serving_team',
    'receiving_team', 'phase', 'home_score_start_of_point', 'visiting_score_start_of_point', 'rally_number', "custom_code",
    "possesion_number"
]
