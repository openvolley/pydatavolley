import pandas as pd


def filteringAttack(plays):
    filtered_plays = plays[(plays['skill'] == 'Attack') & (plays['point_phase'] == 'Reception') & (plays['reception_quality'].str.contains('Perfect|Positive'))]
    result = filtered_plays.groupby('team')['evaluation'].apply(lambda x: (x == 'Winning attack').mean()).reset_index(name='kill_rate')
    print(result)

def firstTransAttack(plays):
    reception_phase = plays[plays['skill'] == "Reception"].groupby(['match_id', 'rally_number']).agg(possesion_number=('possesion_number', 'min')).reset_index()
    reception_phase['possesion_number'] += 1
    reception_phase['is_fta'] = True

  
    plays = pd.merge(plays, reception_phase[['match_id', 'rally_number', 'possesion_number', 'is_fta']], on=['match_id', 'rally_number', 'possesion_number'], how='left')
    plays['is_fta'] = plays['is_fta'].fillna(False)
    return plays