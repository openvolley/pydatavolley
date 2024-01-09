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

def get_match(rows_list):
    # Find the index of [3MATCH]
    match_data = {}
    match_index = rows_list.index('[3MATCH]\n')
    match_row = rows_list[match_index + 1].strip().split(";")
    match_data["day"] = [match_row[0]]
    match_data["time"] =  [match_row[1]]
    match_data["season"] = [match_row[2]]
    match_data["championship"] = [match_row[3]]
    return pd.DataFrame(match_data)

def get_set(rows_list):
    sets_index = rows_list.index('[3SET]\n')
    sets_data = []
    sets_label = ["set","home1","visitor1","home2","visitor2","home3","visitor3", "home4", "visitor4", "duration"]
    for idx in range(1,6):
        rowdata = rows_list[sets_index + idx].strip().split(";")
        set_data = []
        set_data.append(idx) #set number
        add = True
        try:
            set_data.append(int(rowdata[1].split("-")[0])) #1st quarter set IDX home 
            set_data.append(int(rowdata[1].split("-")[1])) #1st quarter set IDX visitor 
            set_data.append(int(rowdata[2].split("-")[0])) #2st quarter set IDX home 
            set_data.append(int(rowdata[2].split("-")[1])) #2st quarter set IDX visitor
            set_data.append(int(rowdata[3].split("-")[0])) #3st quarter set IDX home 
            set_data.append(int(rowdata[3].split("-")[1])) #3st quarter set IDX visitor
            set_data.append(int(rowdata[4].split("-")[0])) #4st quarter set IDX home 
            set_data.append(int(rowdata[4].split("-")[1]))#4st quarter set IDX visitor
        except Exception as e:
            for notidx in range(9):
                set_data.append(None) #1st quarter set IDX home 
                add = False
        
        if (add):
            set_data.append(int(rowdata[5]))
        
        sets_data.append(set_data)
    return(pd.DataFrame(data=sets_data,columns=sets_label))

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
    'player_id', 'skill', 'skill_type', 'evaluation_code', 'setter_position', 'evaluation', 'attack_code', 'attack_description',
    'set_code', 'set_description', 'set_type', 'start_zone', 'end_zone', 'end_subzone', 'end_cone', 'skill_subtype',
    'num_players', 'num_players_numeric', 'special_code', 'timeout', 'end_of_set', 'substitution', 'point',
    'home_team_score', 'visiting_team_score', 'home_setter_position', 'visiting_setter_position', 'custom_code',
    'home_p1', 'home_p2', 'home_p3', 'home_p4', 'home_p5', 'home_p6', 'visiting_p1', 'visiting_p2',
    'visiting_p3', 'visiting_p4', 'visiting_p5', 'visiting_p6', 'start_coordinate', 'mid_coordinate', 'end_coordinate',
    'point_phase', 'attack_phase', 'start_coordinate_x', 'start_coordinate_y', 'mid_coordinate_x', 'mid_coordinate_y',
    'end_coordinate_x', 'end_coordinate_y', 'home_player_id1', 'home_player_id2', 'home_player_id3', 'home_player_id4',
    'home_player_id5', 'home_player_id6', 'visiting_player_id1', 'visiting_player_id2', 'visiting_player_id3',
    'visiting_player_id4', 'visiting_player_id5', 'visiting_player_id6', 'set_number', 'home_team','visiting_team', 
    'home_team_id', 'visiting_team_id', 'team_id', 'point_won_by', 'winning_attack', 'serving_team', 'receiving_team', 
    'phase', 'home_score_start_of_point', 'visiting_score_start_of_point', 'rally_number', "possesion_number"
    ]

def dv_index2xy(i):
    x = ((i - 1 - np.floor((i - 1) / 100) * 100) / 99) * 3.7125 + 0.14375
    y = (np.floor((i - 1) / 100) / 100) * 7.4074 - 0.2037
    return np.column_stack((x, y))

def add_xy(data):
    data['start_coordinate'] = pd.to_numeric(data['start_coordinate'], errors='coerce')
    data['start_coordinate'] = data['start_coordinate'].astype('Int64')
    data['start_coord_xy'] = data['start_coordinate'].apply(dv_index2xy)
    data[['start_coordinate_x', 'start_coordinate_y']] = pd.DataFrame(data['start_coord_xy'].apply(lambda x: x[0]).tolist())

    data['mid_coordinate'] = pd.to_numeric(data['mid_coordinate'], errors='coerce')
    data['mid_coordinate'] = data['mid_coordinate'].astype('Int64')
    data['mid_coord_xy'] = data['mid_coordinate'].apply(dv_index2xy)
    data[['mid_coordinate_x', 'mid_coordinate_y']] = pd.DataFrame(data['mid_coord_xy'].apply(lambda x: x[0]).tolist())

    data['end_coordinate'] = pd.to_numeric(data['end_coordinate'], errors='coerce')
    data['end_coordinate'] = data['end_coordinate'].astype('Int64')
    data['end_coord_xy'] = data['end_coordinate'].apply(dv_index2xy)
    data[['end_coordinate_x', 'end_coordinate_y']] = pd.DataFrame(data['end_coord_xy'].apply(lambda x: x[0]).tolist())

    data = data.drop(columns = ['start_coord_xy', 'end_coord_xy', 'mid_coord_xy'])
    return data
