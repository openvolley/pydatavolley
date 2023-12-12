import os
import uuid
import requests
import pandas as pd
import numpy as np
from .get_players_from_md import read_players
from .helpers import get_teams, calculate_skill, skill_map, eval_codes, desired_order

class DataVolley:
    """
    A class for reading and processing DataVolley data from a .dvw file.

    Parameters:
    - file_path (str): The path to the DataVolley file to be processed.

    Attributes:
    - file_path (str): The path to the DataVolley file.
    - plays (pd.DataFrame): Processed data stored in a DataFrame.
    """

    def __init__(self, file_path = None):
        """
        Initialize the DataVolley object.

        Parameters:
        - file_path (str): The path to the DataVolley file to be processed.
        """
        if file_path is None:
            file_path = self._download_example_data()
        self.file_path = file_path
        self._read_data()

    def _download_example_data(self):
        """
        Download example DataVolley data from a URL and save it locally.

        Returns:
        - str: The path to the downloaded example data file.
        """
        example_data_url = "https://raw.githubusercontent.com/bzx24/markov-volleyball/9f1dd80ea3628af9d2e46f24a4afdd74668dfe07/dvw_files/_2019-09-01%20106859%20UL-UD(VM).dvw"
        response = requests.get(example_data_url)
        response.raise_for_status()  # Raise an error for unsuccessful HTTP responses
        
        example_data_path = os.path.join(os.path.dirname(__file__), "example_data.dvw")

        with open(example_data_path, 'w') as file:
            file.write(response.text)

        return example_data_path
        

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

        # Create code, point_phase attack_phase start_coordinate mid_coordinate end_coordinate time set home_rotation visitng_rotation video_file_number video_time
        plays = plays[0].str.split(';', expand = True).rename({0: 'code', 1: 'point_phase', 2: 'attack_phase', 4: 'start_coordinate', 5: 'mid_coordinate', 6: 'end_coordinate', 7: 'time', 8: 'set_number', 9: 'home_setter_position', 10: 'visiting_setter_position', 11: 'video_file_number', 12: 'video_time'}, axis=1)
        plays.columns.values[14:20] = [f"home_p{i+1}" for i in range(6)]
        plays.columns.values[20:26] = [f"visiting_p{i+1}" for i in range(6)]
        plays = plays.drop(columns=([3, 13, 26]))

        # Create match_id
        plays['match_id'] = str(uuid.uuid4())

        # Change coordiantes -1-1
        plays['start_coordinate'] = np.where(plays['start_coordinate'] == '-1-1', np.nan, plays['start_coordinate'])
        plays['mid_coordinate'] = np.where(plays['mid_coordinate'] == '-1-1', np.nan, plays['mid_coordinate'])
        plays['end_coordinate'] = np.where(plays['end_coordinate'] == '-1-1', np.nan, plays['end_coordinate'])

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
        plays['rally_number'] = plays.groupby('set_number', group_keys=False)['skill'].apply(lambda x: (x == 'Serve').cumsum())

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
        plays['home_team_score'] = plays.groupby(['set_number', 'rally_number'])['home_team_score'].bfill()

        # Create visiting_team_score
        plays['visiting_team_score'] = plays[plays['code'].str[1:2] == 'p']['code'].str[5:7]
        plays['visiting_team_score'] = plays.groupby(['set_number', 'rally_number'])['visiting_team_score'].bfill()

        # Create coordinates
        #plays['start_coordinate_x']
        #plays['start_coordinate_y']
        #def dv_index2xy(index=None):
        #    binx = 0.5 + (np.arange(1, 101) - 11) / 80 * 3.0
        #    biny = 0.5 + (np.arange(1, 102) - 11) / 81 * 6.0
        #    binx = binx + (np.diff(binx[:2]) / 2)
        #    biny = biny + (np.diff(biny[:2]) / 2)
        #    cxy = pd.DataFrame(np.array(np.meshgrid(binx, biny)).T.reshape(-1, 2), columns = ['x', 'y'])
        #    if index is None:
        #        return cxy
        #    else:
        #        assert np.issubdtype(index.dtype, np.number)
        #        index = pd.to_numeric(index, errors = 'coerce').astype(float)
        #        index[index < 0] = np.nan
        #        return cxy.iloc[index - 1]

        # Create serving_team
        plays['serving_team'] = np.where((plays['skill'] == 'Serve') & (plays['code'].str[0:1] == '*'), home_team, None)
        plays['serving_team'] = np.where((plays['skill'] == 'Serve') & (plays['code'].str[0:1] == 'a'), visiting_team, plays['serving_team'])
        plays['serving_team'] = plays.groupby(['set_number', 'rally_number'])['serving_team'].ffill()

        # Create receiving_team
        plays['receiving_team'] = np.where(plays['serving_team'] == home_team, visiting_team, home_team)
        plays['receiving_team'] = np.where(plays['serving_team'].isna(), np.nan, plays['receiving_team'])

        # Create point_phase
        plays['point_phase'] = np.where((plays['serving_team'] == plays['team']), 'Serve', 'Reception')

        # Create home_score_start_of_point
        #plays['rally_number'] = plays.groupby('set', group_keys=False)['skill'].apply(lambda x: (x == 'Serve').cumsum())
        #plays['home_team_score'] = plays.groupby(['set', 'rally_number'])['home_team_score'].bfill()

        # Create attack_phase
        plays['attack_phase'] = np.where((plays['skill'] == 'Attack') & (plays['skill'].shift(2) == 'Reception') & (plays['skill'].shift(1) == 'Set') & (plays['team'].shift(2) == plays['team']),'Reception',np.nan)
        plays['attack_phase'] = np.where((plays['skill'] == 'Attack') & (plays['skill'].shift(2) != 'Reception') & (plays['skill'].shift(1) == 'Set') & (plays['serving_team'] != plays['team']) & (plays['team'].shift(2) == plays['team']),'SO-Transition',plays['attack_phase'])
        plays['attack_phase'] = np.where((plays['skill'] == 'Attack') & (plays['skill'].shift(2) != 'Reception') & (plays['skill'].shift(1) == 'Set') & (plays['serving_team'] == plays['team']) & (plays['team'].shift(2) == plays['team']),'BP-Transition',plays['attack_phase'])

        # Create visiting_score_start_of_point

        # Create team_touch_id

        # Create possesion_number
        plays['possesion_number'] = plays.groupby(['set_number', 'rally_number'], group_keys=False)['skill'].apply(lambda x: (x == 'Attack').shift(1).cumsum() + 1).fillna(0).astype(int)

        # Create timeout

        # Create end_of_set

        # Create substitution

        # Create custom code
        plays['custom_code'] = plays['code'].str.split("~", expand=True).iloc[:, 5:8].apply(lambda x: "~".join(filter(None, x)), axis=1)

        # Create file line number

        #self.plays = plays.replace('', np.nan)
        existing_columns = [col for col in desired_order if col in plays.columns]
        plays = plays[existing_columns]
        self.plays = plays.replace('', np.nan)

    def get_plays(self):
        """
        Get the processed plays data.
    
        Returns:
        - pd.DataFrame: Processed data stored in a DataFrame.
        """
        return self.plays
