import pandas as pd 

# https://snippets.openvolley.org/indicators-and-statistics.html


def exSideoutRate(plays):
    lso = plays.loc[plays['skill'] == "Reception"]\
        .groupby('evaluation')\
        .apply(lambda x: pd.Series({'expected_sideout_rate': (x['point_won_by'] == x['team']).mean()}))\
        .reset_index()
    print(lso)


def exSideoutRateByPlayer(plays):
    lso = plays.loc[plays['skill'] == "Reception"]\
        .groupby('evaluation')\
        .apply(lambda x: pd.Series({'expected_sideout_rate': (x['point_won_by'] == x['team']).mean()}))\
        .reset_index()
    merged_plays = pd.merge(plays.loc[plays['skill'] == "Reception"], lso, on="evaluation", how="left")

    result = merged_plays.groupby(['player_id', 'player_name'])\
        .agg(n_receptions=('evaluation', 'size'),
            expected_sideout_rate=('expected_sideout_rate', 'mean'))\
        .reset_index()

    print(result)




def exBreakpointRate(plays):
    lbp = plays.loc[plays['skill'] == "Serve"]\
        .groupby('evaluation')\
        .agg(expected_breakpoint_rate=('team', lambda x: x.eq(plays['point_won_by']).mean()))\
        .reset_index()

    print(lbp) 


def exBreakpointRateByPlayer(plays):

    lbp = plays.loc[plays['skill'] == "Serve"]\
        .groupby('evaluation')\
        .agg(expected_breakpoint_rate=('team', lambda x: x.eq(plays['point_won_by']).mean()))\
        .reset_index()
    
    merged_plays = plays.loc[plays['skill'] == "Serve"]\
        .merge(lbp, on="evaluation", how="left")

    result = merged_plays.groupby(['player_id', 'player_name'])\
        .agg(n_serves=('evaluation', 'size'),
            expected_breakpoint_rate=('expected_breakpoint_rate', 'mean'))\
        .reset_index()

    print(result)




def setAssistRate(plays): 
    # Aggiungi una variabile indicante se un set è stato seguito da un attacco vincente dalla stessa squadra
    plays['set_had_attack_kill'] = (plays['skill'] == "Set") & (plays['skill'].shift(-1) == "Attack") & \
                                (plays['evaluation'].shift(-1) == "Winning attack") & \
                                (plays['team'].shift(-1) == plays['team'])

    # Filtra solo le righe relative ai set
    set_rows = plays[plays['skill'] == "Set"]

    # Raggruppa per 'team' e 'phase' e calcola il tasso di assistenza
    result = set_rows.groupby(['team', 'attack_phase']) \
                    .agg(assist_rate=('set_had_attack_kill', lambda x: np.sum(x) / len(x))) \
                    .reset_index()

    print(result)