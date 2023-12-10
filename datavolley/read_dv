import pandas as pd
import numpy as np
from .get_players_from_md import read_players
from .helpers import get_teams, calculate_skill, skill_map, eval_codes

class DataVolley:
    """
    A class for reading and processing DataVolley data from a .dvw file.

    Parameters:
    - file_path (str): The path to the DataVolley file to be processed.

    Attributes:
    - file_path (str): The path to the DataVolley file.
    - plays (pd.DataFrame): Processed data stored in a DataFrame.
    """

    def __init__(self, file_path):
        """
        Initialize the DataVolley object.

        Parameters:
        - file_path (str): The path to the DataVolley file to be processed.
        """
        self.file_path = file_path
        self._read_data()

    def _read_data(self):
        """
        Read and process the DataVolley file.

        This method reads the file, extracts metadata, and creates a DataFrame
        containing relevant information about plays.
        """
        rows = [] # Initialize lists to store data
        with open(self.file_path, 'r') as file: # Read the file and extract data
            for line in file:
                rows.append(line)

        full_file = pd.DataFrame(rows)
        full_file['meta_group'] = full_file[0].str.extract(r'\[(.*?)\]', expand=False).ffill()

        # Get Player Names
        meta_data = full_file[full_file['meta_group'] != '3SCOUT']

        # Get teams metadata
        teams = get_teams(rows)
        home_team_id = teams[0].split(";")[0]
        visiting_team_id = teams[1].split(";")[0]
        home_team = teams[0].split(";")[1]
        visiting_team = teams[1].split(";")[1]

        # Parse out the [3SCOUT] and keep the rest
        index_of_scout = full_file.index[full_file[0] == '[3SCOUT]\n'][0]

        # Filter everything before and after "[3SCOUT]"
        plays = full_file.iloc[index_of_scout+1:].reset_index(drop = True)

        # Create code, point_phase attack_phase start_coordinate mid_coordainte end_coordainte time set home_rotation visitng_rotation video_file_number video_time
        plays = plays[0].str.split(';', expand = True).rename({0: 'code', 1: 'point_phase', 2: 'attack_phase', 4: 'start_coordinate', 5: 'mid_coordainte', 6: 'end_coordainte', 7: 'time', 8: 'set', 9: 'home_setter_position', 10: 'visiting_setter_position', 11: 'video_file_number', 12: 'video_time'}, axis=1)
        plays.columns.values[14:20] = [f"home_p{i+1}" for i in range(6)]
        plays.columns.values[20:26] = [f"visiting_p{i+1}" for i in range(6)]
        plays = plays.drop(columns=([3, 13, 26]))

        # Change coordiantes -1-1
        plays['start_coordinate'] = np.where(plays['start_coordinate'] == '-1-1', np.nan, plays['start_coordinate'])
        plays['mid_coordainte'] = np.where(plays['mid_coordainte'] == '-1-1', np.nan, plays['mid_coordainte'])
        plays['end_coordainte'] = np.where(plays['end_coordainte'] == '-1-1', np.nan, plays['end_coordainte'])

        # Create team
        plays['team'] = np.where(plays['code'].str[0:1] == '*', home_team, visiting_team)

        # Create player_number
        plays['player_number'] = plays['code'].str[1:3].str.extract(r'(\d{2})').astype(float).fillna(0).astype(int).astype(str)
        plays['player_number'] = np.where(plays['player_number'] == '0', np.nan, plays['player_number'])

        # Create player_name for both teams
        plays = pd.merge(plays, pd.concat(list([read_players(meta_data, home_team, 'H'), 
                                                read_players(meta_data, visiting_team, 'V')])
                                        ), on=['player_number', 'team'], how='left')

        # Create skill
        plays['skill'] = plays.apply(calculate_skill, axis=1)
        plays['skill'] = plays['skill'].map(skill_map)

        # Create evaluation_code
        plays['evaluation_code'] = plays['code'].str[5]
        plays['evaluation_code'] = np.where(plays['evaluation_code'].isin(eval_codes), plays['evaluation_code'], np.nan)

        # Create set_code
        plays['set_code'] = np.where(plays['skill'] == 'Set', plays['code'].str[6:8], np.nan)
        plays['set_code'] = np.where((plays['skill'] == 'Set') & (plays['set_code'] != '~~'), plays['set_code'], np.nan)

        # Create set_type
        plays['set_type'] = np.where(plays['skill'] == 'Set', plays['code'].str[8:9], np.nan)
        plays['set_type'] = np.where((plays['skill'] == 'Set') & (plays['set_type'] != '~~'), plays['set_type'], np.nan)

        # Create attack code
        plays['attack_code'] = plays['code'].str[6:8]
        plays['attack_code'] = np.where((plays['skill'] == 'Attack') & (plays['attack_code'] != '~~'), plays['attack_code'], np.nan)

        # Create num_players_numeric 
        plays['num_players_numeric'] = np.where(plays['skill'] == 'Attack', plays['code'].str[13:14], np.nan)
        plays['num_players_numeric'] = np.where((plays['skill'] == 'Attack') & (plays['num_players_numeric'] != '~~'), plays['num_players_numeric'], np.nan)

        # Create home_team_id
        plays['home_team_id'] = home_team_id
        plays['visiting_team_id'] = visiting_team_id

        # Create start_zone
        plays['start_zone'] = plays['code'].str[9:10]
        plays['start_zone'] = np.where(plays['start_zone'] != '~', plays['start_zone'], np.nan)
        plays['start_zone'] = np.where(plays['start_zone'] == '', np.nan, plays['start_zone'])

        # Create end_zone
        plays['end_zone'] = plays['code'].str[10:11]
        plays['end_zone'] = np.where(plays['end_zone'] != '~', plays['end_zone'], np.nan)
        plays['end_zone'] = np.where(plays['end_zone'] == '', np.nan, plays['end_zone'])

        # Create end_subzone
        plays['end_subzone'] = plays['code'].str[11:12]
        plays['end_subzone'] = np.where(plays['end_subzone'] != '~', plays['end_subzone'], np.nan)
        plays['end_subzone'] = np.where(plays['end_subzone'] == '', np.nan, plays['end_subzone'])

        # Create rally number
        plays['rally_number'] = plays.groupby('set', group_keys=False)['skill'].apply(lambda x: (x == 'Serve').cumsum())

        # Create point_won_by
        plays['point_won_by'] = plays.apply(lambda row: home_team if row['code'][0:2] == '*p' else visiting_team if row['code'][0:2] == 'ap' else None, axis=1)
        plays['point_won_by'] = plays['point_won_by'].bfill()
        plays['point_won_by'] = np.where(plays['code'].str.contains('Up'), np.nan, plays['point_won_by'])
        plays['point_won_by'] = np.select(
            [
                plays['code'].str.contains(r'\*\*1set'),
                plays['code'].str.contains(r'\*\*2set'),
                plays['code'].str.contains(r'\*\*3set'),
                plays['code'].str.contains(r'\*\*4set'),
                plays['code'].str.contains(r'\*\*5set')
            ],
            [np.nan, np.nan, np.nan, np.nan, np.nan],
            plays['point_won_by']
            )

        # Create point on skill
        plays['skill'] = np.where(plays['code'].str[1:2] == 'p', 'Point', plays['skill'])

        # Create home_team_score
        plays['home_team_score'] = plays[plays['code'].str[1:2] == 'p']['code'].str[2:4]
        plays['home_team_score'] = plays.groupby(['set', 'rally_number'])['home_team_score'].bfill()

        # Create visiting_team_score
        plays['visiting_team_score'] = plays[plays['code'].str[1:2] == 'p']['code'].str[5:7]
        plays['visiting_team_score'] = plays.groupby(['set', 'rally_number'])['visiting_team_score'].bfill()

        # Create coordinates

        # Create winning_attack

        # Create serving_team
        plays['serving_team'] = np.where((plays['skill'] == 'Serve') & (plays['code'].str[0:1] == '*'), home_team, None)
        plays['serving_team'] = np.where((plays['skill'] == 'Serve') & (plays['code'].str[0:1] == 'a'), visiting_team, plays['serving_team'])
        plays['serving_team'] = plays.groupby(['set', 'rally_number'])['serving_team'].ffill()

        # Create receiving_team
        plays['receiving_team'] = np.where(plays['serving_team'] == home_team, visiting_team, home_team)
        self.plays = plays.replace('', np.nan)

        # Create phase

        # Create home_score_start_of_point

        # Create visiting_score_start_of_point

        # Create team_touch_id

        # Create video_time

        # Create vieo_file_number

        # Create point_id

        # Create match_id

        # Create timeout

        # Create end_of_set

        # Create substitution

        # Create custom code

        # Create file line number

    def get_plays(self):
        return self.plays
