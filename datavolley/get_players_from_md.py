def read_players(meta_data, team_name, H_or_V):
    columns_to_rename = {
        1: "player_number", 3: "starting_position_set1", 4: "starting_position_set2", 5: "starting_position_set3", 
        6: "starting_position_set4", 7: "starting_position_set5", 8: "player_id", 9: "lastname", 
        10: "firstname", 11: "nickname", 12: "special_role", 13: "role", 14: "foreign"
        }
    team_players = meta_data[(meta_data['meta_group'] == f'3PLAYERS-{H_or_V}') & (meta_data[0] != f'[3PLAYERS-{H_or_V}]\n')][0].str.split(';', expand = True)
    team_players.columns = [columns_to_rename[col] if col in columns_to_rename else col for col in team_players.columns]

    # Trim whitespace from nickname, firstname, and lastname
    team_players['nickname'] = team_players['nickname'].str.strip()
    team_players['firstname'] = team_players['firstname'].str.strip()
    team_players['lastname'] = team_players['lastname'].str.strip()

    # Replace NA values in nickname, firstname, and lastname with empty strings
    team_players['nickname'].fillna("", inplace=True)
    team_players['firstname'].fillna("", inplace=True)
    team_players['lastname'].fillna("", inplace=True)

    # Trim whitespace from firstname and lastname again after replacing NA values
    team_players['firstname'] = team_players['firstname'].str.strip()
    team_players['lastname'] = team_players['lastname'].str.strip()

    # Create a new 'name' column by concatenating firstname and lastname with a space separator
    team_players['player_name'] = team_players['firstname'] + ' ' + team_players['lastname']

    idx = team_players[team_players['player_name'].apply(lambda x: not bool(x))].index

    # If there are such indices, replace 'name' with "Unnamed player" followed by a sequence number
    if len(idx) > 0:
        team_players.loc[idx, 'player_name'] = ["Unnamed player " + str(i + 1) for i in range(len(idx))]

    # Trim whitespace from 'player_id', 'starting_position_set1', 'starting_position_set2', 'starting_position_set3', 'starting_position_set4', 'starting_position_set5'
    columns_to_trim = ['player_id', 'starting_position_set1', 'starting_position_set2', 'starting_position_set3', 'starting_position_set4', 'starting_position_set5']
    team_players[columns_to_trim] = team_players[columns_to_trim].apply(lambda x: x.str.strip())

    # Replace NA values in 'foreign' with False
    team_players['foreign'].fillna(False, inplace=True)

    # Convert 'number' column to integer
    team_players['number'] = team_players['player_number'].astype(str)

    team_players['team'] = team_name
    team_players = team_players[['player_number', 'player_id', 'player_name', 'team']]
    return team_players