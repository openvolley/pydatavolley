import os
import uuid
import requests
import pandas as pd
import numpy as np
from .get_players_from_md import read_players
from .helpers import get_match, get_set, get_teams, calculate_skill, skill_map, eval_codes, desired_order, add_xy
from charset_normalizer import from_path

class DataVolley:
    """
    A class for reading and processing DataVolley data from a .dvw file.

    Parameters:
    - file_path (str): The path to the DataVolley file to be processed.

    Attributes:
    - file_path (str): The path to the DataVolley file.
    - plays (pd.DataFrame): Processed data stored in a DataFrame.
    - match_info (pd.DataFrame): Data of the match
    - sets_info (pd.DataFrame): Data of each quarter set and duration
    - home_team (str): The name of the home team.
    - home_team_id (str): Unique identifier of the home team. 
    - home_coaches (list): List of the names of the coaches of the home team.
    - visiting_team (str): The name of the visiting team.
    - visiting_team_id (str): Unique identifier of the visiting team. 
    - visiting_team_coaches (list): List of the names of the coaches of the visiting team.
    - get_players (pd.DataFrame): Retrieves a DataFrame containing a list of players from a specified team, or from all teams if none is specified.
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
        self.match_info = None
        self.sets_info = None
        self.home_team = ""
        self.home_team_id = ""
        self.home_setswon = 0
        self.visiting_team = ""
        self.visiting_team_id = ""
        self.visiting_setswon = 0
        self.visiting_coaches = []
        self.home_coaches = []
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

        # identify character encoding
        results = from_path(self.file_path)
        rows = [] # Initialize lists to store data
        with open(self.file_path, 'r',encoding=results.best().encoding) as file: # Read the file and extract data
            for line in file:
                rows.append(line)

        full_file = pd.DataFrame(rows)
        full_file['meta_group'] = full_file[0].str.extract(r'\[(.*?)\]', expand=False).ffill()

        # Get Match information
        self.match_info = get_match(rows)
        self.sets_info = get_set(rows)

        # Get teams metadata
        teams = get_teams(rows)
        self.home_team_id = teams[0].split(";")[0]
        self.home_team = teams[0].split(";")[1]
        self.home_setswon = int(teams[0].split(";")[2]) 
        self.home_coaches = []
        self.home_coaches.append(teams[0].split(';')[3])
        self.home_coaches.append(teams[0].split(';')[4])
        self.visiting_team_id = teams[1].split(";")[0]
        self.visiting_team = teams[1].split(";")[1]
        self.visiting_setswon = int(teams[1].split(";")[2])
        self.visiting_coaches = []
        self.visiting_coaches.append(teams[1].split(';')[3])
        self.visiting_coaches.append(teams[1].split(';')[4])

        # Get Player Names
        meta_data = full_file[full_file['meta_group'] != '3SCOUT']
        datarows = []
        for idx, row in  meta_data[meta_data.meta_group == "3PLAYERS-H"].iterrows():
            rowtext = row[0].rstrip()
            if (rowtext.find(";")> 0):
                datarows.append(rowtext.split(";")[:13])
        self.players_home = pd.DataFrame(data=datarows,
                               columns=["team_id","player_number","team",
                                        "set1","set2","set3","set4","set5",
                                        "player_id","lastname","name",
                                        "nickname","role"])
        self.players_home['team_id'] = self.home_team_id
        self.players_home['team'] = self.home_team
        self.players_home["player_name"] = self.players_home["name"] + " " + self.players_home["lastname"]
        datarows = []
        for idx, row in  meta_data[meta_data.meta_group == "3PLAYERS-V"].iterrows():
            rowtext = row[0].rstrip()
            if (rowtext.find(";")> 0):
                datarows.append(rowtext.split(";")[:13])
        self.players_visiting = pd.DataFrame(data=datarows,
                               columns=["team_id","player_number","team",
                                        "set1","set2","set3","set4","set5",
                                        "player_id","lastname","name",
                                        "nickname","role"])
        self.players_visiting['team_id'] = self.visiting_team_id
        self.players_visiting['team'] = self.visiting_team
        self.players_visiting["player_name"] = self.players_visiting["name"] + " " + self.players_visiting["lastname"]
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
        def replace_coordinates(coord):
            coordinates_to_replace = {'-1-1': np.nan}
            return coordinates_to_replace.get(coord, coord)

        plays['start_coordinate'] = plays['start_coordinate'].map(replace_coordinates)
        plays['mid_coordinate'] = plays['mid_coordinate'].map(replace_coordinates)
        plays['end_coordinate'] = plays['end_coordinate'].map(replace_coordinates)


        # Create team
        plays['team'] = np.where(plays['code'].str[0:1] == '*', self.home_team, self.visiting_team)

        # Create player_number
        plays['player_number'] = plays['code'].str[1:3].str.extract(r'(\d{2})').astype(float).fillna(0).astype(int).astype(str)
        plays['player_number'] = np.where(plays['player_number'] == '0', np.nan, plays['player_number'])

        # Create player_name for both teams
        plays = pd.merge(plays, pd.concat(list([read_players(meta_data, self.home_team, 'H'), 
                                                read_players(meta_data, self.visiting_team, 'V')])
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
        plays['home_team_id'] = self.home_team_id
        plays['visiting_team_id'] = self.visiting_team_id

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
        plays['point_won_by'] = plays.apply(lambda row: self.home_team if row['code'][0:2] == '*p' else self.visiting_team if row['code'][0:2] == 'ap' else None, axis=1)
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
        plays['home_team_score'] = pd.to_numeric(plays['home_team_score'], errors='coerce')
        plays['home_team_score'] = plays['home_team_score'].astype('Int64')

        # Create visiting_team_score
        plays['visiting_team_score'] = plays[plays['code'].str[1:2] == 'p']['code'].str[5:7]
        plays['visiting_team_score'] = plays.groupby(['set_number', 'rally_number'])['visiting_team_score'].bfill()
        plays['visiting_team_score'] = pd.to_numeric(plays['visiting_team_score'], errors='coerce')
        plays['visiting_team_score'] = plays['visiting_team_score'].astype('Int64')

        # Create coordinates
        plays = add_xy(plays)

        # Create serving_team
        plays['serving_team'] = np.where((plays['skill'] == 'Serve') & (plays['code'].str[0:1] == '*'), self.home_team, None)
        plays['serving_team'] = np.where((plays['skill'] == 'Serve') & (plays['code'].str[0:1] == 'a'), self.visiting_team, plays['serving_team'])
        plays['serving_team'] = plays.groupby(['set_number', 'rally_number'])['serving_team'].ffill()

        # Create receiving_team
        plays['receiving_team'] = np.where(plays['serving_team'] == self.home_team, self.visiting_team, self.home_team)
        plays['receiving_team'] = np.where(plays['serving_team'].isna(), np.nan, plays['receiving_team'])

        # Create point_phase
        plays['point_phase'] = np.where((plays['serving_team'] == plays['team']), 'Serve', 'Reception')

        # Create attack_phase
        plays['attack_phase'] = np.where((plays['skill'] == 'Attack') & (plays['skill'].shift(2) == 'Reception') & (plays['skill'].shift(1) == 'Set') & (plays['team'].shift(2) == plays['team']),'Reception', np.NaN)
        plays['attack_phase'] = np.where((plays['skill'] == 'Attack') & (plays['skill'].shift(2) != 'Reception') & (plays['skill'].shift(1) == 'Set') & (plays['serving_team'] != plays['team']) & (plays['team'].shift(2) == plays['team']),'SO-Transition',plays['attack_phase'])
        plays['attack_phase'] = np.where((plays['skill'] == 'Attack') & (plays['skill'].shift(2) != 'Reception') & (plays['skill'].shift(1) == 'Set') & (plays['serving_team'] == plays['team']) & (plays['team'].shift(2) == plays['team']),'BP-Transition',plays['attack_phase'])

        # Create possesion_number
        plays['possesion_number'] = plays.groupby(['set_number', 'rally_number'], group_keys=False)['skill'].apply(lambda x: (x == 'Attack').shift(1).cumsum() + 1).fillna(0).astype(int)

        # Create timeout

        # Create end_of_set

        # Create home_score_start_of_point

        # Create visiting_score_start_of_point

        # Create substitution

        # Create home_team
        plays['home_team'] = self.home_team

        # Create visiting_team
        plays['visiting_team'] = self.visiting_team

        # Create setter_position
        plays['setter_position'] = np.where(plays['home_team'] == plays['team'], plays['home_setter_position'], plays['visiting_setter_position'])

        # Create custom code
        plays['custom_code'] = plays['code'].apply(lambda x: x.rsplit('~', 1)[1] if '~' in x else None)

        # Reorder columns
        existing_columns = [col for col in desired_order if col in plays.columns]
        plays = plays[existing_columns]
        self.plays = plays
        plays = plays.replace({np.nan: None})
        return plays

    def get_plays(self):
        """
        Get the processed plays data.

        Returns:
        - pd.DataFrame: Processed data stored in a DataFrame.
        """
        return self.plays

    def get_players(self,team=None):
        """
        Retrieves a DataFrame containing a list of players from a specified team, or from all teams if none is specified.

        Args:
            team (str, optional): The name or the id of the team to filter players for. If None, players from all teams are returned.

         Returns:
                pd.DataFrame: A DataFrame containing the filtered players. 
                If 'team' is specified, the DataFrame will contain only players from that team. 
                If there are no players for the specified team, the DataFrame is returned with both teams.
        """
        players = pd.concat([self.players_home,self.players_visiting],ignore_index=True)
        if team != None:
            if ((team == self.home_team) or (team == self.home_team_id)):
                players = self.players_home
            if ((team == self.visiting_team) or (team == self.visiting_team_id)):
                players = self.players_visiting
        return players
