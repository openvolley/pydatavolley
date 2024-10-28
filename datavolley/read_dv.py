"""Main module to manage the datavolley files"""
import os
import uuid
import random
import requests
import pandas as pd
import numpy as np
from charset_normalizer import from_path
from .get_players_from_md import read_players
from .helpers import get_match, get_set, get_teams,\
            calculate_skill, skill_map, eval_codes,\
            desired_order, add_xy, get_setter_calls,\
            get_attack_combinations


class DataVolley:
    """
    A class for reading and processing DataVolley data from a .dvw file.

    Parameters:
    - file_path (str): The path to the DataVolley file to be processed.

    Attributes:
    - file_path (str): 
        The path to the DataVolley file.
    - plays (pd.DataFrame):
        Processed data stored in a DataFrame.
    - match_info (pd.DataFrame):
        Data of the match
    - sets_info (pd.DataFrame):
        Data of each quarter set and duration
    - home_team (str):
        The name of the home team.
    - home_team_id (str):
        Unique identifier of the home team. 
    - home_coaches (list):
        List of the names of the coaches of the home team.
    - visiting_team (str):
        The name of the visiting team.
    - visiting_team_id (str):
        Unique identifier of the visiting team. 
    - visiting_team_coaches (list):
        List of the names of the coaches of the visiting team.
    - get_players (pd.DataFrame): 
        Retrieves a DataFrame containing a list of players
        from a specified team, or from all teams if none is specified.
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
        dvw_files = [
            "_2019-08-30 109691 PITT-CINCI(VM).dvw",
            "_2019-08-30 118402 IUPUI-USD(VM).dvw",
            "_2019-08-31 106857 UL-TAMU(VM).dvw",
            "_2019-08-31 109692 PITT-USC(VM).dvw",
            "_2019-08-31 117367 IUPUI-MURR(VM).dvw",
            "_2019-09-01 104145 TEXAS-USC(VM).dvw",
            "_2019-09-01 106859 UL-UD(VM).dvw",
            "_2019-09-01 108282 UNL-UCLA(VM).dvw",
            "_2019-09-05 104147 TEXAS-UMN(VM).dvw",
            "_2019-09-06 106862 UL-TTU(VM).dvw",
            "_2019-09-06 106883 UL-WKU(VM).dvw",
            "_2019-08-30 109691 PITT-CINCI(VM).dvw",
            "_2019-08-30 118402 IUPUI-USD(VM).dvw",
            "_2019-08-31 106857 UL-TAMU(VM).dvw",
            "_2019-08-31 109692 PITT-USC(VM).dvw",
            "_2019-08-31 117367 IUPUI-MURR(VM).dvw",
            "_2019-09-06 110424 UNL-UA(VM).dvw",
            "_2019-09-07 106887 UL-ASU(VM).dvw",
            "_2019-09-07 107789 EKU-NCA_T(VM).dvw",
            "_2019-09-07 109693 PITT-UWGB(VM).dvw",
            "_2019-09-07 109719 PITT-OSU(VM).dvw",
            "_2019-09-07 113907 EKU-DART(VM).dvw",
            "_2019-09-07 120692 WISC-BAY(VM).dvw",
            "_2019-09-08 109694 PITT-DUQ(VM).dvw",
            "_2019-09-12 109695 PITT-ORE(VM).dvw",
            "_2019-09-13 106889 UL-PURD(VM).dvw",
            "_2019-09-13 108182 EKU-SHU(VM).dvw",
            "_2019-09-13 108456 WISC-USC(VM).dvw",
            "_2019-09-13 120134 PITT-CPOLY(VM).dvw",
            "_2019-09-13 121081 BAY-UH(VM) (13).dvw",
            "_2019-09-13 122154 UNL-HPU(VM).dvw",
            "_2019-09-13 122188 FAMU-SJ(VM).dvw",
            "_2019-09-14 106474 STAN-UMN(VM).dvw",
            "_2019-09-14 108302 UNL-UD(VM).dvw",
            "_2019-09-14 108306 UNL-LMU(VM).dvw",
            "_2019-09-14 12import random0300 UW-UNO(VM).dvw",
            "_2019-09-14 121003 BAY-UT(VM) (13).dvw",
            "_2019-09-14 122296 TAMIU-WNMU(VM).dvw",
            "_2019-09-14 122306 FAMU-SBU(VM).dvw",
            "_2019-09-17 101165 EKU-MARSH(VM).dvw",
            "_2019-09-19 108314 UNL-STAN(VM).dvw",
            "_2019-09-20 105860 IUPUI-MSU(VM).dvw",
            "_2019-09-20 109796 WISC-UW(VM).dvw",
            "_2019-09-20 117560 FAMU-SUBR(VM).dvw",
            "_2019-09-20 123093 BAY-UM(VM) (13).dvw",
            "_2019-09-21 104148 TEXAS-TAMU(VM).dvw",
            "_2019-09-21 104647 APSU-WSU(VM).dvw",
            "_2019-09-21 106770 STAN-BYU(VM).dvw",
            "_2019-09-21 108316 UNL-WSU(VM).dvw",
            "_2019-09-21 117561 FAMU-CIT(VM).dvw",
            "_2019-09-21 123054 EKU-DUQ(VM).dvw",
            "_2019-09-22 103573 UW-WISC(VM).dvw",
            "_2019-09-22 109696 PITT-PSU(VM).dvw",
            "_2019-09-24 124060 BAY-TXST(VM) (12).dvw",
            "_2019-09-26 104152 TEXAS-ISU(VM).dvw",
            "_2019-09-27 106891 UL-NCST(VM).dvw",
            "_2019-09-27 113953 EKU-TSU(VM).dvw",
            "_2019-09-27 118774 IUPUI-CSU(VM).dvw",
            "_2019-09-27 121715 TAMIU-DBU(VM).dvw",
            "_2019-09-28 104154 TEXAS-TTU(VM).dvw",
            "_2019-09-28 109797 WISC-PURD(VM).dvw",
            "_2019-09-28 118775 IUPUI-OAK(VM).dvw",
            "_2019-09-28 121716 TAMIU-TSU(VM).dvw",
            "_2019-09-28 124666 EKU-BEL(VM).dvw",
            "_2019-09-29 106771 STAN-UW(VM).dvw",
            "_2019-09-29 106894 UL-UNC(VM).dvw",
            "_2019-09-29 109697 PITT-VT(VM).dvw",
            "_2019-09-29 109798 WISC-IU(VM).dvw",
            "_2019-10-03 109799 WISC-PSU(VM).dvw",
            "_2019-10-03 125913 BAY-OU(VM) (13).dvw",
            "_2019-10-04 106898 UL-GT(VM).dvw",
            "_2019-10-04 127391 APSU-SEMO(VM).dvw",
            "_2019-10-05 121718 TAMIU-TAMUK(VM).dvw",
            "_2019-10-05 127568 APSU-UTM(VM).dvw",
            "_2019-10-06 106901 UL-CLEM(VM).dvw",
            "_2019-10-06 108323 UNL-WISC(VM).dvw",
            "_2019-10-09 118776 IUPUI-YSU(VM).dvw",
            "_2019-10-09 129743 APSU-MURR(VM).dvw",
            "_2019-10-12 103574 UW-ORST(VM).dvw",
            "_2019-10-12 104156 TEXAS-OU(VM).dvw",
            "_2019-10-12 106772 STAN-UA(VM).dvw",
            "_2019-10-12 108325 UNL-MSU(VM).dvw",
            "_2019-10-12 130152 EKU-MURR(VM).dvw",
            "_2019-10-13 103575 UW-ORE(VM).dvw",
            "_2019-10-13 106773 STAN-ASU(VM).dvw",
            "_2019-10-13 107800 FAMU-NCA_T(VM).dvw",
            "_2019-10-13 108326 UNL-MICH(VM).dvw",
            "_2019-10-13 109800 WISC-UMN(VM).dvw",
            "_2019-10-17 108327 UNL-PURD(VM).dvw",
            "_2019-10-18 109698 PITT-UNC(VM).dvw",
            "_2019-10-18 121719 TAMIU-UAFS(VM).dvw",
            "_2019-10-18 133155 APSU-TSU(VM).dvw",
            "_2019-10-19 103576 UW-ASU(VM).dvw",
            "_2019-10-19 106774 STAN-COL(VM).dvw",
            "_2019-10-19 109155 TAMIU-CU(VM).dvw",
            "_2019-10-19 109801 WISC-ILL(VM).dvw",
            "_2019-10-19 125009 APSU-BEL(VM).dvw",
            "_2019-10-19 125915 BAY-TTU(VM) (14).dvw",
            "_2019-10-20 103577 UW-UA(VM).dvw",
            "_2019-10-20 106775 STAN-UofU(VM).dvw",
            "_2019-10-20 109802 WISC-NU(VM).dvw",
            "_2019-10-20 140524 FAMU-MORG(VM).dvw",
            "_2019-10-24 104157 TEXAS-BAY(VM).dvw",
            "_2019-10-25 106909 UL-UVA(VM).dvw",
            "_2019-10-25 134437 EKU-SIUE(VM).dvw",
            "_2019-10-26 118777 IUPUI-WSU(VM).dvw",
            "_2019-10-26 125916 BAY-WVU(VM) (13).dvw",
            "_2019-10-26 134539 EKU-EIU(VM).dvw",
            "_2019-10-27 106913 UL-PITT(VM).dvw",
            "_2019-10-27 118778 IUPUI-NKU(VM).dvw",
            "_2019-10-31 109803 WISC-UMD(VM).dvw",
            "_2019-11-01 109701 PITT-WF(VM).dvw",
            "_2019-11-01 118780 IUPUI-UIC(VM).dvw",
            "_2019-11-01 121720 TAMIU-ENMU(VM).dvw",
            "_2019-11-01 136019 APSU-SIUE(VM).dvw",
            "_2019-11-02 103578 UW-USC(VM).dvw",
            "_2019-11-02 104158 TEXAS-WVU(VM).dvw",
            "_2019-11-02 108329 UNL-RU(VM).dvw",
            "_2019-11-02 114177 TAMIU-WTAMU(VM).dvw",
            "_2019-11-02 118781 IUPUI-MILW(VM).dvw",
            "_2019-11-02 136020 APSU-EIU(VM).dvw",
            "_2019-11-03 103579 UW-UCLA(VM).dvw",
            "_2019-11-03 106777 STAN-ORE(VM).dvw",
            "_2019-11-03 108332 UNL-PSU(VM).dvw",
            "_2019-11-03 109703 PITT-DUKE(VM).dvw",
            "_2019-11-03 135811 BAY-ISU(VM) (14).dvw",
            "_2019-11-07 108339 UNL-NU(VM).dvw",
            "_2019-11-08 137198 EKU-JSU(VM).dvw",
            "_2019-11-09 109706 PITT-GT(VM).dvw",
            "_2019-11-09 137297 EKU-TTU(VM).dvw",
            "_2019-11-10 109711 PITT-CLEM(VM).dvw",
            "_2019-11-10 118779 IUPUI-UWGB(VM).dvw",
            "_2019-11-13 137945 EKU-MORE(VM).dvw",
            "_2019-11-14 104159 TEXAS-KSU(VM).dvw",
            "_2019-11-14 137312 BAY-KU(VM) (13).dvw",
            "_2019-11-15 138188 TAMIU-SEU(VM).dvw",
            "_2019-11-16 103600 UW-COL(VM).dvw",
            "_2019-11-16 106778 STAN-USC(VM).dvw",
            "_2019-11-16 106918 UL-CUSE(VM).dvw",
            "_2019-11-16 121722 TAMIU-SMUT(VM).dvw",
            "_2019-11-16 138176 APSU-EKU(VM).dvw",
            "_2019-11-17 103580 UW-UofU(VM).dvw",
            "_2019-11-17 104160 TEXAS-TCU(VM).dvw",
            "_2019-11-17 106779 STAN-UCLA(VM).dvw",
            "_2019-11-17 108341 UNL-IOWA(VM).dvw",
            "_2019-11-17 109804 WISC-MSU(VM).dvw",
            "_2019-11-21 137313 BAY-TEXAS(VM) (12).dvw",
            "_2019-11-22 109712 PITT-FSU(VM).dvw",
            "_2019-11-23 106923 UL-ND(VM).dvw",
            "_2019-11-23 129824 WISC-IOWA(VM).dvw",
            "_2019-11-24 104161 TEXAS-KU(VM).dvw",
            "_2019-11-24 106928 UL-MIA(VM).dvw",
            "_2019-11-24 109805 WISC-UNL(VM).dvw",
            "_2019-11-27 103601 UW-CAL(VM).dvw",
            "_2019-11-27 109715 PITT-UL(VM).dvw",
            "_2019-11-29 106780 STAN-CAL(VM).dvw",
            "_2019-11-29 139393 MARQ-VILL(VM).dvw",
            "_2019-11-30 108342 UNL-UMD(VM).dvw",
            "_2019-11-30 137315 BAY-TCU(VM) (14).dvw",
            "_2019-11-30 139726 MARQ-SJ(VM).dvw",
            "_2019-12-01 103602 UW-WSU(VM).dvw",
            "_2019-12-01 108344 UNL-OSU(VM).dvw",
            "_2019-12-05 140244 UL-SAM(VM).dvw",
            "_2019-12-06 139796 MARQ-UD(VM).dvw",
            "_2019-12-06 140246 TEXAS-ALB(VM).dvw",
            "_2019-12-07 139847 STAN-UD(VM).dvw",
            "_2019-12-07 139864 UW-WU(VM).dvw",
            "_2019-12-07 139994 UNL-BSU(VM).dvw",
            "_2019-12-07 140118 PITT-HOW(VM).dvw",
            "_2019-12-07 140138 BAY-SHU(VM) (14).dvw",
            "_2019-12-07 140249 TEXAS-UCSB(VM).dvw",
            "_2019-12-07 140270 WISC-ILLST(VM).dvw",
            "_2019-12-08 139997 UNL-UM(VM).dvw",
            "_2019-12-08 140297 WISC-UCLA(VM).dvw",
            "_2019-12-08 140301 PITT-CINCI(VM).dvw",
            "_2019-12-08 140312 STAN-CPOLY(VM).dvw",
            "_2019-12-08 140315 BAY-USC(VM) (16).dvw",
            "_2019-12-08 140316 UW-USC(VM).dvw",
            "_2019-12-13 140335 TEXAS-UL(VM).dvw",
            "_2019-12-13 140383 BAY-PURD(VM) (13).dvw",
            "_2019-12-13 140384 UW-UK(VM).dvw",
            "_2019-12-13 140601 UNL-UH(VM).dvw",
            "_2019-12-13 140603 WISC-TAMU(VM).dvw",
            "_2019-12-14 140664 STAN-UofU(VM).dvw",
            "_2019-12-14 140727 WISC-UNL(VM).dvw",
            "_2019-12-14 140755 BAY-UW(VM) (18).dvw",
            "_2019-12-15 140754 STAN-PSU(VM).dvw",
            "_2019-12-20 140895 BAY-WISC(VM) (17).dvw",
            "_2019-12-20 140896 STAN-UMN(VM).dvw",
            "_2019-12-22 141609 STAN-WISC(VM).dvw"
            ]
        base_url = "https://raw.githubusercontent.com/bzx24/markov-volleyball/master/dvw_files/"
        random_file = random.choice(dvw_files)
        example_data_url = base_url + random_file
        response = requests.get(example_data_url,timeout=60)
        response.raise_for_status()  # Raise an error for unsuccessful HTTP responses
        example_data_path = os.path.join(os.path.dirname(__file__), "example_data.dvw")
        with open(example_data_path, 'w',encoding="utf-8") as file:
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
        # Read the file and extract data
        enc = results.best().encoding
        with open(self.file_path, 'r',encoding=enc) as file:
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


        # identify the index for the markers "[3ATTACKCOMBINATION]" and "[3SETTERCALL]"
        index_of_attack_combination = full_file.index[full_file[0] == '[3ATTACKCOMBINATION]\n'][0]
        index_of_setter_call = full_file.index[full_file[0] == '[3SETTERCALL]\n'][0]

        # Filter the rows from "[3ATTACKCOMBINATION]" to "[3SETTERCALL]" (exclude external)
        filtered_plays = full_file.iloc[index_of_attack_combination + 1\
                :index_of_setter_call].reset_index(drop=True)

        separated_data = filtered_plays[0].str.split(';', expand=True)

        # create a dictionary code: description (code 1st column, description 5th)
        try:
            play_dict = dict(zip(separated_data[0], separated_data[4]))
        except KeyError as e:
            print(f"Error: {e}. check the columns")
            play_dict = None

        # Get Player Names
        meta_data = full_file[full_file['meta_group'] != '3SCOUT']
        datarows = []
        for _, row in  meta_data[meta_data.meta_group == "3PLAYERS-H"].iterrows():
            rowtext = row[0].rstrip()
            if rowtext.find(";")> 0:
                datarows.append(rowtext.split(";")[:13])
        self.players_home = pd.DataFrame(data=datarows,
                columns=["team_id","player_number","team",
                        "set1","set2","set3","set4","set5",
                        "player_id","lastname","name",
                        "nickname","role"])
        self.players_home['team_id'] = self.home_team_id
        self.players_home['team'] = self.home_team
        self.players_home["player_name"] = self.players_home["name"] +\
              " " + self.players_home["lastname"]
        datarows = []
        for _, row in  meta_data[meta_data.meta_group == "3PLAYERS-V"].iterrows():
            rowtext = row[0].rstrip()
            if rowtext.find(";")> 0:
                datarows.append(rowtext.split(";")[:13])
        self.players_visiting = pd.DataFrame(data=datarows,
                               columns=["team_id","player_number","team",
                                        "set1","set2","set3","set4","set5",
                                        "player_id","lastname","name",
                                        "nickname","role"])
        self.players_visiting['team_id'] = self.visiting_team_id
        self.players_visiting['team'] = self.visiting_team
        self.players_visiting["player_name"] = \
            self.players_visiting["name"] + " " +\
            self.players_visiting["lastname"]
        # Parse out the [3SCOUT] and keep the rest
        index_of_scout = full_file.index[full_file[0] == '[3SCOUT]\n'][0]

        # Filter everything before and after "[3SCOUT]"
        plays = full_file.iloc[index_of_scout+1:].reset_index(drop = True)

        # Create code, point_phase attack_phase start_coordinate 
        # mid_coordinate end_coordinate time set home_rotation 
        # visiting_rotation video_file_number video_time
        plays = plays[0].str.split(';', expand = True)\
            .rename({0: 'code', 1: 'point_phase',\
                    2: 'attack_phase', 4: 'start_coordinate',\
                    5: 'mid_coordinate', 6: 'end_coordinate',\
                    7: 'time', 8: 'set_number', \
                    9: 'home_setter_position', 10: 'visiting_setter_position',\
                    11: 'video_file_number', 12: 'video_time'}, axis=1)
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
        plays['player_number'] = plays['code'].str[1:3].str.extract(r'(\d{2})')\
            .astype(float).fillna(0).astype(int).astype(str)
        plays['player_number'] = np.where(plays['player_number'] == '0',\
            np.nan, plays['player_number'])

        # Create player_name for both teams
        plays = pd.merge(plays, pd.concat(list([read_players(meta_data, self.home_team, 'H'), 
                                                read_players(meta_data, self.visiting_team, 'V')])
                                        ), on=['player_number', 'team'], how='left')

        # Create skill
        plays['skill'] = plays.apply(calculate_skill, axis=1)
        plays['skill'] = plays['skill'].map(skill_map)

        # Create evaluation_code
        plays['evaluation_code'] = plays['code'].str[5]
        plays['evaluation_code'] =\
            np.where(plays['evaluation_code'].isin(eval_codes), plays['evaluation_code'], np.nan)

        # Create set_code
        plays['set_code'] =\
            np.where(plays['skill'] == 'Set', plays['code'].str[6:8], np.nan)
        plays['set_code'] =\
            np.where((plays['skill'] == 'Set') &\
            (plays['set_code'] != '~~'), plays['set_code'], np.nan)

        # Create set_type
        plays['set_type'] = np.where(plays['skill'] == 'Set',\
            plays['code'].str[8:9], np.nan)
        plays['set_type'] = np.where((plays['skill'] == 'Set') &\
            (plays['set_type'] != '~~'), plays['set_type'], np.nan)

        # Create attack code
        plays['attack_code'] = plays['code'].str[6:8]
        plays['attack_code'] =\
            np.where((plays['skill'] == 'Attack') &\
            (plays['attack_code'] != '~~'), plays['attack_code'], np.nan)

        # Create num_players_numeric
        plays['num_players_numeric'] =\
            np.where(plays['skill'] == 'Attack',\
            plays['code'].str[13:14], np.nan)
        plays['num_players_numeric'] =\
            np.where((plays['skill'] == 'Attack') &\
            (plays['num_players_numeric'] != '~~'), plays['num_players_numeric'], np.nan)

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
        plays['rally_number'] =\
            plays.groupby('set_number', group_keys=False)['skill']\
            .apply(lambda x: (x == 'Serve').cumsum())

        # Create point_won_by
        plays['point_won_by'] = plays.apply(lambda row: self.home_team\
            if row['code'][0:2] == '*p'\
            else self.visiting_team\
            if row['code'][0:2] == 'ap'\
            else None, axis=1)
        plays['point_won_by'] = plays['point_won_by'].bfill()
        plays['point_won_by'] =\
            np.where(plays['code'].str.contains('Up'),\
            np.nan, plays['point_won_by'])
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
        plays['home_team_score'] =\
            plays[plays['code'].str[1:2] == 'p']['code'].str[2:4]
        plays['home_team_score'] =\
            plays.groupby(['set_number', 'rally_number'])['home_team_score'].bfill()
        plays['home_team_score'] =\
            pd.to_numeric(plays['home_team_score'], errors='coerce')
        plays['home_team_score'] =\
            plays['home_team_score'].astype('Int64')

        # Create visiting_team_score
        plays['visiting_team_score'] =\
            plays[plays['code'].str[1:2] == 'p']['code'].str[5:7]
        plays['visiting_team_score'] =\
            plays.groupby(['set_number', 'rally_number'])['visiting_team_score'].bfill()
        plays['visiting_team_score'] =\
            pd.to_numeric(plays['visiting_team_score'], errors='coerce')
        plays['visiting_team_score'] =\
            plays['visiting_team_score'].astype('Int64')
        # Create coordinates
        plays = add_xy(plays)
        # Create serving_team
        plays['serving_team'] = \
            np.where((plays['skill'] == 'Serve') &\
            (plays['code'].str[0:1] == '*'), self.home_team, None)
        plays['serving_team'] =\
            np.where((plays['skill'] == 'Serve') &\
            (plays['code'].str[0:1] == 'a'),\
            self.visiting_team, plays['serving_team'])
        plays['serving_team'] =\
            plays.groupby(['set_number',\
            'rally_number'])['serving_team'].ffill()

        # Create receiving_team
        plays['receiving_team'] =\
            np.where(plays['serving_team'] == \
            self.home_team, self.visiting_team, self.home_team)
        plays['receiving_team'] = \
            np.where(plays['serving_team'].isna(), np.nan, plays['receiving_team'])

        # Create point_phase
        plays['point_phase'] = \
            np.where((plays['serving_team'] == plays['team']), 'Serve', 'Reception')

        # Create attack_phase
        plays['attack_phase'] = \
        np.where((plays['skill'] == 'Attack') &\
        (plays['skill'].shift(2) == 'Reception') &\
        (plays['skill'].shift(1) == 'Set') &\
        (plays['team'].shift(2) == plays['team']),'Reception', np.nan)

        plays['attack_phase'] =\
            np.where((plays['skill'] == 'Attack') &\
            (plays['skill'].shift(2) != 'Reception') &\
            (plays['skill'].shift(1) == 'Set') &\
            (plays['serving_team'] != plays['team']) &\
            (plays['team'].shift(2) == plays['team']),'SO-Transition',plays['attack_phase'])
 
        plays['attack_phase'] = \
            np.where((plays['skill'] == 'Attack') &\
            (plays['skill'].shift(2) != 'Reception') &\
            (plays['skill'].shift(1) == 'Set') &\
            (plays['serving_team'] == plays['team']) &\
            (plays['team'].shift(2) == plays['team']),'BP-Transition',plays['attack_phase'])

        # Create possesion_number
        plays['possesion_number'] = \
            plays.groupby(['set_number', 'rally_number'],\
            group_keys=False)['skill']\
            .apply(lambda x: (x == 'Attack')\
            .shift(1).cumsum() + 1).fillna(0).astype(int)

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
        plays['setter_position'] =\
            np.where(plays['home_team'] == plays['team'],\
            plays['home_setter_position'], plays['visiting_setter_position'])

        # Create custom code
        plays['custom_code'] = \
            plays['code'].apply(lambda x: \
                x.rsplit('~', 1)[1] if '~' in x else None)

        # Mappatura dei codici di valutazione
        evaluation_mapping = {
            "Serve": {"=": "Error", 
                      "/": "Positive, no attack", 
                      "-": "Negative, opponent free attack", 
                      "+": "Positive, opponent some attack",
                      "#": "Ace", 
                      "!": "OK, no first tempo possible"},
            "Reception": 
                {"=": "Error", "/": "Poor, no attack", 
                 "-": "Negative, limited attack", 
                "+": "Positive, attack", "#": "Perfect pass",
                 "!": "OK, no first tempo possible"},
            "Attack": 
                {"=": "Error", "/": "Blocked",
                 "-": "Poor, easily dug", 
                 "!": "Blocked for reattack",
                 "+": "Positive, good attack",
                 "#": "Winning attack"},
            "Block": 
                {"=": "Error", "/": "Invasion",
                 "-": "Poor, opposition to replay", 
                "+": "Positive, block touch", 
                "#": "Winning block", 
                "!": "Poor, opposition to replay"},
            "Dig": 
                {"=": "Error", "/": "Ball directly back over net",
                 "-": "No structured attack possible", 
                "#": "Perfect dig", "+": "Good dig", 
                "!": "OK, no first tempo possible"},
            "Set": 
                {"=": "Error", "-": "Poor", 
                 "/": "Poor", 
                "+": "Positive", "#": "Perfect",
                "!": "OK"},
            "Freeball": 
                {"=": "Error", "/": "Poor",
                 "!": "OK, no first tempo possible", 
                "-": "OK, only high set possible",
                "+": "Good", "#": "Perfect"}
        }

        # add the column "evaluation"
        plays['evaluation'] =\
            plays.apply(lambda row: evaluation_mapping.\
                get(row['skill'], {}).get(row['evaluation_code'], ""), axis=1)

        # add the column "Attack_Description"
        if play_dict is not None:
            plays['attack_description'] = plays['attack_code'].map(play_dict)

        # Add shoot type
        plays["skill_type "] = plays.apply(lambda row: row['code'][4] if len(row['code']) > 4 else None, axis=1)

        # Add attack combinations
        attack_combinations = get_attack_combinations(rows)
        plays['attack_description'] = plays.apply(lambda row: attack_combinations.get(row['attack_code'], ""), axis=1)

        # Add setter calls
        setter_calls = get_setter_calls(rows)
        plays['set_description'] = plays.apply(lambda row: setter_calls.get(row['set_code'], ""), axis=1)


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
        Retrieves a DataFrame containing a list of players 
        from a specified team, or from all teams if none is specified.

        Args:
            team (str, optional): 
            The name or the id of the team to filter players for. 
            If None, players from all teams are returned.

         Returns:
                pd.DataFrame: A DataFrame containing the filtered players. 
                If 'team' is specified, the DataFrame will contain only 
                players from that team. 
                If there are no players for the specified team, 
                the DataFrame is returned with both teams.
        """
        players = pd.concat([self.players_home,self.players_visiting],ignore_index=True)
        if team is not None:
            if ((team == self.home_team) or (team == self.home_team_id)):
                players = self.players_home
            if ((team == self.visiting_team) or (team == self.visiting_team_id)):
                players = self.players_visiting
        return players
