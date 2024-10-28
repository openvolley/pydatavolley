"""Helpers to support read_dv.py"""
import pandas as pd
import numpy as np

# Function to extract teams
def get_teams(rows_list):
    """
    Extracts and returns the home team and visiting team from the provided list of rows.

    Args:
        rows_list (list of str): A list of strings where each string is a line from a file.

    Returns:
        tuple: A tuple containing two elements:
            - home_team (str): The name of the home team.
            - visiting_team (str): The name of the visiting team.

    Example:
        rows_list = [
            "Some other data\n",
            "[3TEAMS]\n",
            "Home Team Name\n",
            "Visiting Team Name\n",
            "Some more data\n"
        ]
        home_team, visiting_team = get_teams(rows_list)
        print(home_team)  # Output: Home Team Name
        print(visiting_team)  # Output: Visiting Team Name
    """
     # Find the index of [3TEAMS]
    teams_index = rows_list.index('[3TEAMS]\n')
    # Extract home_team and visiting_team
    home_team = rows_list[teams_index + 1].strip()
    visiting_team = rows_list[teams_index + 2].strip()
    return home_team, visiting_team

def get_attack_combinations(rows_list):
    """
    Extracts and processes attack combinations from a list of rows.

    Parameters:
    rows_list (Any): A list containing rows with attack data. The type can be adjusted 
                     based on the structure of rows_list if it is more specific than 'Any'.

    Returns:
    dict: A dictionary containing the processed attack combinations.

    The function iterates over the provided rows list, analyzes the data to identify
    various attack combinations, and stores them in a dictionary format.
    """
    # Find the index of [3ATTACKCOMBINATION]
    attack_combinations_index = rows_list.index('[3ATTACKCOMBINATION]\n')
    # Extract attack_combinations
    attack_combinations = {}
    for idx in range(1, len(rows_list)):
        if rows_list[attack_combinations_index + idx] == '[3SETTERCALL]\n':
            break
        splitted_combinations = rows_list[attack_combinations_index + idx + 1].strip().split(";")
        attack_combinations[splitted_combinations[0]] = splitted_combinations[4] if len(splitted_combinations) > 4 else None
    return attack_combinations

def get_setter_calls(rows_list):
    """
    Extracts and processes setter calls from a list of rows.

    Parameters:
    rows_list (Any): A list containing rows with setter call data. 
                     The type can be adjusted if 'rows_list' is more specific than 'Any'.

    Returns:
    dict: A dictionary containing the processed setter call data.

    The function iterates over the provided rows list, identifies setter calls,
    and stores them in a dictionary format, organizing the data for further analysis.
    """
    # Find the index of [3SETTERCALL]
    setter_calls_index = rows_list.index('[3SETTERCALL]\n')
    # Extract setter_calls
    setter_calls = {}
    for idx in range(1, len(rows_list)):
        if rows_list[setter_calls_index + idx] == '[3WINNINGSYMBOLS]\n':
            break
        splitted_calls = rows_list[setter_calls_index + idx + 1].strip().split(";")
        setter_calls[splitted_calls[0]] = splitted_calls[2] if len(splitted_calls) > 2 else None
    return setter_calls

def get_match(rows_list):
    """
    Extracts match data from the provided list of rows 
    and returns it as an instance of Match_data class.

    Args:
        rows_list (list of str): A list of strings where 
        each string is a line from a file.

    Returns:
        Match_data: An instance of the Match_data 
        class containing match details.

    The Match_data class has the following attributes:
        - day (str): The day of the match.
        - season (str): The season in which the match is played.
        - time (str): The time of the match.
        - championship (str): The championship name.

    Example:
        rows_list = [
            "Some other data\n",
            "[3MATCH]\n",
            "2024-06-22;18:00;2024;Championship Name\n",
            "Some more data\n"
        ]
        match_data = get_match(rows_list)
        print(match_data.day)           # Output: 2024-06-22
        print(match_data.time)          # Output: 18:00
        print(match_data.season)        # Output: 2024
        print(match_data.championship)  # Output: Championship Name
    """
    # Find the index of [3MATCH]
    # this is the class returned to avoid the use of a dataframe to extract the information
    class Matchdata:
        """
        A class to represent match data.

        Attributes:
            day (str): The day of the match.
            season (str): The season in which the match is played.
            time (str): The time of the match.
            championship (str): The championship name.
        """

        def __init__(self, day="", season="", time="", championship=""):
            """
            Initialize the Matchdata object with day, season, time, and championship.
            """
            self.day = day
            self.season = season
            self.time = time
            self.championship = championship
        def get_match_info(self):
            """
            Returns a summary of the match data.
            
            Returns:
                str: A string containing the match information.
            """
            return f"{self.day} {self.time}, {self.championship}, {self.season}"
        def is_match_today(self, current_day):
            """
            Check if the match is scheduled for today.
            
            Args:
                current_day (str): The current day.
            
            Returns:
                bool: True if the match is today, False otherwise.
            """
            return self.day == current_day

    match_index = rows_list.index('[3MATCH]\n')
    match_row = rows_list[match_index + 1].strip().split(";")
    match_data = Matchdata(match_row[0],match_row[2],match_row[1],match_row[3])
    return match_data

def get_set(rows_list):
    """
    Extracts set data from the provided list of rows and returns it as a pandas DataFrame.

    Args:
        rows_list (list of str): A list of strings where each string is a line from a file.

    Returns:
        pandas.DataFrame: A DataFrame containing the set data with the following columns:
            - set (int): The set number.
            - home1 (int or NA): Home team score in the 1st quarter.
            - visitor1 (int or NA): Visitor team score in the 1st quarter.
            - home2 (int or NA): Home team score in the 2nd quarter.
            - visitor2 (int or NA): Visitor team score in the 2nd quarter.
            - home3 (int or NA): Home team score in the 3rd quarter.
            - visitor3 (int or NA): Visitor team score in the 3rd quarter.
            - home4 (int or NA): Home team score in the 4th quarter.
            - visitor4 (int or NA): Visitor team score in the 4th quarter.
            - duration (int or NA): Duration of the set.

    Example:
        rows_list = [
            "Some other data\n",
            "[3SET]\n",
            "25-23;20-25;25-20;25-18;15-12\n",
            "Some more data\n"
        ]
        df = get_set(rows_list)
        print(df)
    """
    sets_index = rows_list.index('[3SET]\n')
    sets_data = []
    sets_label = ["set","home1",\
                "visitor1","home2",\
                "visitor2","home3",\
                "visitor3", "home4",\
                "visitor4", "duration"]
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
        except ValueError:
            for _ in range(9):
                set_data.append(pd.NA) #add quarter set NAN
                add = False
        if add:
            set_data.append(int(rowdata[5]))
        sets_data.append(set_data)

    df = pd.DataFrame(data=sets_data,columns=sets_label)
    contains_any_nan = df.isna().any().any()
    if contains_any_nan:
        df_cleaned = df.dropna(subset=[col for col in df.columns if col != 'set'], how='all')
        cols_to_convert = ['home1', 'visitor1',\
                           'home2', 'visitor2',\
                           'home3', 'visitor3',\
                            'home4', 'visitor4', 'duration']
        for col in cols_to_convert:
            df_cleaned.loc[:, col] = pd.to_numeric(df_cleaned[col], errors='coerce').astype('Int64')
        df = df_cleaned
    return df

def get_base_attack(row):
    """
    Extracts the base attack value from a given row of data.

    Parameters:
    row (Any): A row containing data from which the base attack value is to be extracted.
               The type can be adjusted if 'row' has a more specific structure.

    Returns:
    string | None: The base attack value extracted from the row. 
            The function returns a string if a valid base value is found,
            a different type if other data is present, or None if no value is applicable.

    This function processes a single row to determine the base attack metric,
    depending on the structure and content of the row.
    """
    if pd.isna(row['player_number']):
        return np.nan
    code = row['code'][3]
    bs = None
    if code.find("E") > -1:
        bs = code[6:8]
    return bs

# get player number out of code
def calculate_skill(row):
    """
    Extracts the skill code from the 'code' field 
    if the 'player_number' field is not NaN.

    Args:
        row (pd.Series): 
        A pandas Series object representing a row 
        of data with 'player_number' and 'code' fields.

    Returns:
        str or float: 
        The skill code extracted from the 'code' field
        (fourth character) if 'player_number' is not NaN.
        Returns NaN if 'player_number' is NaN.

    Example:
        row = pd.Series({'player_number': 7, 'code': 'ABC1XYZ'})
        skill = calculate_skill(row)
        print(skill)  # Output: 1

        row_with_nan = pd.Series({'player_number': np.nan, 'code': 'ABC1XYZ'})
        skill = calculate_skill(row_with_nan)
        print(skill)  # Output: nan
    """
    if pd.isna(row['player_number']):
        return np.nan
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
    'match_id', 'point_id', 'video_file_number', 
    'video_time', 'code', 'team', 'player_number', 
    'player_name', 'player_id', 'skill', 'skill_type', 
    'evaluation_code', 'setter_position', 'evaluation', 
    'attack_code', 'attack_description', 'set_code', 
    'set_description', 'set_type', 'start_zone', 'end_zone', 
    'end_subzone', 'end_cone', 'skill_subtype',
    'num_players', 'num_players_numeric', 'special_code', 
    'timeout', 'end_of_set', 'substitution', 'point',
    'home_team_score', 'visiting_team_score', 'home_setter_position', 
    'visiting_setter_position', 'custom_code', 'home_p1', 'home_p2', 
    'home_p3', 'home_p4', 'home_p5', 'home_p6', 'visiting_p1',
    'visiting_p2', 'visiting_p3', 'visiting_p4', 'visiting_p5',
    'visiting_p6', 'start_coordinate', 'mid_coordinate', 'end_coordinate',
    'point_phase', 'attack_phase', 'start_coordinate_x', 'start_coordinate_y',
    'mid_coordinate_x', 'mid_coordinate_y', 'end_coordinate_x', 
    'end_coordinate_y', 'home_player_id1', 'home_player_id2', 
    'home_player_id3', 'home_player_id4', 'home_player_id5', 'home_player_id6', 
    'visiting_player_id1', 'visiting_player_id2', 'visiting_player_id3',
    'visiting_player_id4', 'visiting_player_id5', 'visiting_player_id6', 
    'set_number', 'home_team','visiting_team', 
    'home_team_id', 'visiting_team_id', 'team_id', 'point_won_by', 
    'winning_attack', 'serving_team', 'receiving_team', 
    'phase', 'home_score_start_of_point', 'visiting_score_start_of_point', 
    'rally_number', "possesion_number"
    ]

def dv_index2xy(i):
    """
    Converts a given index to x and y coordinates 
    based on a specific transformation formula.

    Args:
        i (int or array-like): 
        Index or array of indices to be converted.

    Returns:
        np.ndarray: 
        A 2D numpy array where each row contains the x 
        and y coordinates corresponding to the input index.

    Example:
        index = 150
        coordinates = dv_index2xy(index)
        print(coordinates)
        # Output: array([[0.5225 , 0.34438]])

        indices = [1, 50, 150]
        coordinates = dv_index2xy(indices)
        print(coordinates)
        # Output: array([[ 0.14375 , -0.2037  ],
        #                [ 1.86562 , -0.2037  ],
        #                [ 0.5225  ,  0.34438 ]])
    """
    x = ((i - 1 - np.floor((i - 1) / 100) * 100) / 99) * 3.7125 + 0.14375
    y = (np.floor((i - 1) / 100) / 100) * 7.4074 - 0.2037
    return np.column_stack((x, y))

def add_xy(data):
    """
    Adds x and y coordinate columns to the DataFrame 
    based on start, mid, and end coordinate indices.

    Args:
        data (pd.DataFrame): DataFrame containing 
        'start_coordinate', 'mid_coordinate', 
        and 'end_coordinate' columns.

    Returns:
        pd.DataFrame: The input DataFrame with added
        columns for x and y coordinates of start, 
        mid, and end points.

    The following columns will be added to the DataFrame:
        - 'start_coordinate_x', 'start_coordinate_y'
        - 'mid_coordinate_x', 'mid_coordinate_y'
        - 'end_coordinate_x', 'end_coordinate_y'

    Example:
        data = pd.DataFrame({
            'start_coordinate': [150, 300],
            'mid_coordinate': [350, 400],
            'end_coordinate': [450, 500]
        })
        data = add_xy(data)
        print(data)
        # Output:
        #    start_coordinate  mid_coordinate   [..]    end_coordinate_y
        # 0              150            350     [..]    0.33784
        # 1              300            400     [..]    0.69136
    """
    data['start_coordinate'] = pd.to_numeric(data['start_coordinate'], errors='coerce')
    data['start_coordinate'] = data['start_coordinate'].astype('Int64')
    data['start_coord_xy'] = data['start_coordinate'].apply(dv_index2xy)
    data[['start_coordinate_x', 'start_coordinate_y']] =\
        pd.DataFrame(data['start_coord_xy'].apply(lambda x: x[0]).tolist())
    data['mid_coordinate'] = pd.to_numeric(data['mid_coordinate'], errors='coerce')
    data['mid_coordinate'] = data['mid_coordinate'].astype('Int64')
    data['mid_coord_xy'] = data['mid_coordinate'].apply(dv_index2xy)
    data[['mid_coordinate_x', 'mid_coordinate_y']] =\
        pd.DataFrame(data['mid_coord_xy'].apply(lambda x: x[0]).tolist())

    data['end_coordinate'] = pd.to_numeric(data['end_coordinate'], errors='coerce')
    data['end_coordinate'] = data['end_coordinate'].astype('Int64')
    data['end_coord_xy'] = data['end_coordinate'].apply(dv_index2xy)
    data[['end_coordinate_x', 'end_coordinate_y']] =\
        pd.DataFrame(data['end_coord_xy'].apply(lambda x: x[0]).tolist())

    data = data.drop(columns = ['start_coord_xy', 'end_coord_xy', 'mid_coord_xy'])
    return data
