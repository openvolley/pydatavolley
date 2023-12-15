# pydatavolley

A python package for reading volleyball scouting files in DataVolley
format (\*.dvw).

<https://pypi.org/project/pydatavolley/>

### Installation[^1]

    pip install pydatavolley
    pip install --upgrade pydatavolley

## <u>Examples</u>

#### Reading one file:

``` python
# Using read_dv.DataVolley(None) will use example file
import pandas as pd
from datavolley import read_dv
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 400)
dv_instance = read_dv.DataVolley(None)
df = dv_instance.get_plays()
print(df[588:618])
```

                                     match_id video_file_number video_time                code                      team player_number      player_name player_id      skill evaluation_code setter_position attack_code set_code set_type start_zone end_zone end_subzone num_players_numeric  home_team_score  visiting_team_score home_setter_position visiting_setter_position custom_code home_p1 home_p2  \
    588  2385b493-00c8-4535-b784-ccfced4d58df                 1       2231   a10SM-~~~17A~~~+2      University of Dayton            10   Jamie Peterson    -11802      Serve               -               3         NaN      NaN      NaN          1        7           A                 NaN                5                    6                    5                        3          +2      11      15   
    589  2385b493-00c8-4535-b784-ccfced4d58df                 1       2232  *10RM#~~~17AW~~-2F  University of Louisville            10      Mel McHenry    -75967  Reception               #               5         NaN      NaN      NaN          1        7           A                 NaN                5                    6                    5                        3         -2F      11      15   
    590  2385b493-00c8-4535-b784-ccfced4d58df                 1       2233   *19EQ#K1C~3B~~~-2  University of Louisville            19  Shannon Shields   -296094        Set               #               5         NaN       K1        C        NaN        3           B                 NaN                5                    6                    5                        3          -2      11      15   
    591  2385b493-00c8-4535-b784-ccfced4d58df                 1       2234  *07AQ-X1~37AT2~-2F  University of Louisville             7      Emily Scott   -224837     Attack               -               5          X1      NaN      NaN          3        7           A                   2                5                    6                    5                        3         -2F      11      15   
    592  2385b493-00c8-4535-b784-ccfced4d58df                 1       2234  a02DQ+~~~37AS~~+2B      University of Dayton             2    Maura Collins   -230138        Dig               +               3         NaN      NaN      NaN          3        7           A                 NaN                5                    6                    5                        3         +2B      11      15   
    593  2385b493-00c8-4535-b784-ccfced4d58df                 1       2236   a08ET#K1F~8A~~~+2      University of Dayton             8  Brooke Westbeld   -232525        Set               #               3         NaN       K1        F        NaN        8           A                 NaN                5                    6                    5                        3          +2      11      15   
    594  2385b493-00c8-4535-b784-ccfced4d58df                 1       2237  a05AT+X5~46CH2~+2F      University of Dayton             5      Alli Papesh   -230141     Attack               +               3          X5      NaN      NaN          4        6           C                   2                5                    6                    5                        3         +2F      11      15   
    595  2385b493-00c8-4535-b784-ccfced4d58df                 1       2238  *09DT-~~~46CS~~-2B  University of Louisville             9  Claire Chaussee   -225496        Dig               -               5         NaN      NaN      NaN          4        6           C                 NaN                5                    6                    5                        3         -2B      11      15   
    596  2385b493-00c8-4535-b784-ccfced4d58df                 1       2240  a15AO+~~~34BT1~+2F      University of Dayton            15     Rachael Fara   -273640     Attack               +               3         NaN      NaN      NaN          3        4           B                   1                5                    6                    5                        3         +2F      11      15   
    597  2385b493-00c8-4535-b784-ccfced4d58df                 1       2240  *10DO-~~~34BS~~-2F  University of Louisville            10      Mel McHenry    -75967        Dig               -               5         NaN      NaN      NaN          3        4           B                 NaN                5                    6                    5                        3         -2F      11      15   
    598  2385b493-00c8-4535-b784-ccfced4d58df                 1       2241  a03FH+~~~49C~~~+2B      University of Dayton             3  Elizabeth House   -230142   Freeball               +               3         NaN      NaN      NaN          4        9           C                 NaN                5                    6                    5                        3         +2B      11      15   
    599  2385b493-00c8-4535-b784-ccfced4d58df                 1       2243   a08EN#KBC~3D~~~+2      University of Dayton             8  Brooke Westbeld   -232525        Set               #               3         NaN       KB        C        NaN        3           D                 NaN                5                    6                    5                        3          +2      11      15   
    600  2385b493-00c8-4535-b784-ccfced4d58df                 1       2244  a15AN-CF~28AP2~+2F      University of Dayton            15     Rachael Fara   -273640     Attack               -               3          CF      NaN      NaN          2        8           A                   2                5                    6                    5                        3         +2F      11      15   
    601  2385b493-00c8-4535-b784-ccfced4d58df                 1       2245  *19DN+~~~28AS~~-2B  University of Louisville            19  Shannon Shields   -296094        Dig               +               5         NaN      NaN      NaN          2        8           A                 NaN                5                    6                    5                        3         -2B      11      15   
    602  2385b493-00c8-4535-b784-ccfced4d58df                 1       2247   *08EH#~~~~7B~~~-2  University of Louisville             8    Lexi Hamilton    -75970        Set               #               5         NaN      NaN        ~        NaN        7           B                 NaN                5                    6                    5                        3          -2      11      15   
    603  2385b493-00c8-4535-b784-ccfced4d58df                 1       2248  *10AH+V5~41CP2~-2F  University of Louisville            10      Mel McHenry    -75967     Attack               +               5          V5      NaN      NaN          4        1           C                   2                5                    6                    5                        3         -2F      11      15   
    604  2385b493-00c8-4535-b784-ccfced4d58df                 1       2249  a10DH-~~~41CS~~+2B      University of Dayton            10   Jamie Peterson    -11802        Dig               -               3         NaN      NaN      NaN          4        1           C                 NaN                5                    6                    5                        3         +2B      11      15   
    605  2385b493-00c8-4535-b784-ccfced4d58df                 1       2252  *09FH+~~~68B~~~-2B  University of Louisville             9  Claire Chaussee   -225496   Freeball               +               5         NaN      NaN      NaN          6        8           B                 NaN                5                    6                    5                        3         -2B      11      15   
    606  2385b493-00c8-4535-b784-ccfced4d58df                 1       2253   *19ET#K1B~2C~~~-2  University of Louisville            19  Shannon Shields   -296094        Set               #               5         NaN       K1        B        NaN        2           C                 NaN                5                    6                    5                        3          -2      11      15   
    607  2385b493-00c8-4535-b784-ccfced4d58df                 1       2254  *15AT#X6~25CH4~-2F  University of Louisville            15       Aiko Jones   -224838     Attack               #               5          X6      NaN      NaN          2        5           C                   4                5                    6                    5                        3         -2F      11      15   
    608  2385b493-00c8-4535-b784-ccfced4d58df                 1       2254   a15BT=~~~~4C~~~+2      University of Dayton            15     Rachael Fara   -273640      Block               =               3         NaN      NaN      NaN        NaN        4           C                 NaN                5                    6                    5                        3          +2      11      15   
    609  2385b493-00c8-4535-b784-ccfced4d58df                 1       2255             *p05:06  University of Louisville           NaN              NaN       NaN      Point             NaN               5         NaN      NaN      NaN        NaN      NaN         NaN                 NaN                5                    6                    5                        3        None      11      15   
    610  2385b493-00c8-4535-b784-ccfced4d58df                 1       2281             *c15:12  University of Louisville           NaN              NaN       NaN        NaN             NaN               0         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             <NA>                 <NA>                    0                        0        None      \n    None   
    611  2385b493-00c8-4535-b784-ccfced4d58df                 1       2281             *c19:25  University of Louisville           NaN              NaN       NaN        NaN             NaN               0         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             <NA>                 <NA>                    0                        0        None      \n    None   
    612  2385b493-00c8-4535-b784-ccfced4d58df                 1       2281                *P25  University of Louisville           NaN              NaN       NaN        NaN             NaN               4         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             <NA>                 <NA>                    4                        3        None      12      10   
    613  2385b493-00c8-4535-b784-ccfced4d58df                 1       2281                 *z4  University of Louisville           NaN              NaN       NaN        NaN             NaN               4         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             <NA>                 <NA>                    4                        3        None      12      10   
    614  2385b493-00c8-4535-b784-ccfced4d58df                 1       2281                aP08      University of Dayton           NaN              NaN       NaN        NaN             NaN               3         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             <NA>                 <NA>                    4                        3        None      12      10   
    615  2385b493-00c8-4535-b784-ccfced4d58df                 1       2281                 az3      University of Dayton           NaN              NaN       NaN        NaN             NaN               3         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             <NA>                 <NA>                    4                        3        None      12      10   
    616  2385b493-00c8-4535-b784-ccfced4d58df                 1       2281   *12SM+~~~56C~~~-1  University of Louisville            12      Tori Dilfer   -263069      Serve               +               4         NaN      NaN      NaN          5        6           C                 NaN                5                    7                    4                        3          -1      12      10   
    617  2385b493-00c8-4535-b784-ccfced4d58df                 1       2282  a03RM-~~~56CW~~+1B      University of Dayton             3  Elizabeth House   -230142  Reception               -               3         NaN      NaN      NaN          5        6           C                 NaN                5                    7                    4                        3         +1B      12      10   

        home_p3 home_p4 home_p5 home_p6 visiting_p1 visiting_p2 visiting_p3 visiting_p4 visiting_p5 visiting_p6  start_coordinate  mid_coordinate  end_coordinate point_phase   attack_phase start_coordinate_x start_coordinate_y mid_coordinate_x mid_coordinate_y end_coordinate_x end_coordinate_y set_number                 home_team         visiting_team home_team_id visiting_team_id  \
    588      10       7      19       9          10          15           8           5          16           3               577            <NA>            7369       Serve            nan            2.99375            0.16667             <NA>             <NA>          2.69375         5.203702          2  University of Louisville  University of Dayton           17               42   
    589      10       7      19       9          10          15           8           5          16           3               577            <NA>            7369   Reception            nan            2.99375            0.16667             <NA>             <NA>          2.69375         5.203702          2  University of Louisville  University of Dayton           17               42   
    590      10       7      19       9          10          15           8           5          16           3              4456            <NA>            <NA>   Reception            nan            2.20625           3.055556             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42   
    591      10       7      19       9          10          15           8           5          16           3              4546            <NA>            7075   Reception      Reception            1.83125            3.12963             <NA>             <NA>          2.91875          4.98148          2  University of Louisville  University of Dayton           17               42   
    592      10       7      19       9          10          15           8           5          16           3              4546            <NA>            7075       Serve            nan            1.83125            3.12963             <NA>             <NA>          2.91875          4.98148          2  University of Louisville  University of Dayton           17               42   
    593      10       7      19       9          10          15           8           5          16           3              2959            <NA>            <NA>       Serve            nan            2.31875           1.944446             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42   
    594      10       7      19       9          10          15           8           5          16           3              4315            <NA>            8150       Serve  BP-Transition            0.66875           2.981482             <NA>             <NA>          1.98125         5.796294          2  University of Louisville  University of Dayton           17               42   
    595      10       7      19       9          10          15           8           5          16           3              4315            <NA>            8150   Reception            nan            0.66875           2.981482             <NA>             <NA>          1.98125         5.796294          2  University of Louisville  University of Dayton           17               42   
    596      10       7      19       9          10          15           8           5          16           3              4550            <NA>            5572       Serve            nan            1.98125            3.12963             <NA>             <NA>          2.80625          3.87037          2  University of Louisville  University of Dayton           17               42   
    597      10       7      19       9          10          15           8           5          16           3              4550            <NA>            5572   Reception            nan            1.98125            3.12963             <NA>             <NA>          2.80625          3.87037          2  University of Louisville  University of Dayton           17               42   
    598      10       7      19       9          10          15           8           5          16           3              4528            <NA>            6827       Serve            nan            1.15625            3.12963             <NA>             <NA>          1.11875         4.833332          2  University of Louisville  University of Dayton           17               42   
    599      10       7      19       9          10          15           8           5          16           3              4243            <NA>            <NA>       Serve            nan            1.71875           2.907408             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42   
    600      10       7      19       9          10          15           8           5          16           3              4684            <NA>            7043       Serve  BP-Transition            3.25625           3.203704             <NA>             <NA>          1.71875          4.98148          2  University of Louisville  University of Dayton           17               42   
    601      10       7      19       9          10          15           8           5          16           3              4684            <NA>            7043   Reception            nan            3.25625           3.203704             <NA>             <NA>          1.71875          4.98148          2  University of Louisville  University of Dayton           17               42   
    602      10       7      19       9          10          15           8           5          16           3              3230            <NA>            <NA>   Reception            nan            1.23125           2.166668             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42   
    603      10       7      19       9          10          15           8           5          16           3              4321            <NA>            8127   Reception  SO-Transition            0.89375           2.981482             <NA>             <NA>          1.11875         5.796294          2  University of Louisville  University of Dayton           17               42   
    604      10       7      19       9          10          15           8           5          16           3              4321            <NA>            8127       Serve            nan            0.89375           2.981482             <NA>             <NA>          1.11875         5.796294          2  University of Louisville  University of Dayton           17               42   
    605      10       7      19       9          10          15           8           5          16           3              1857            <NA>            6742   Reception            nan            2.24375           1.129632             <NA>             <NA>          1.68125         4.759258          2  University of Louisville  University of Dayton           17               42   
    606      10       7      19       9          10          15           8           5          16           3              4570            <NA>            <NA>   Reception            nan            2.73125            3.12963             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42   
    607      10       7      19       9          10          15           8           5          16           3              4484            5484            8084   Reception  SO-Transition            3.25625           3.055556          3.25625         3.796296          3.25625          5.72222          2  University of Louisville  University of Dayton           17               42   
    608      10       7      19       9          10          15           8           5          16           3              4616            <NA>            <NA>       Serve            nan            0.70625           3.203704             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42   
    609      10       7      19       9          10          15           8           5          16           3              1807            <NA>            <NA>   Reception            nan            0.36875           1.129632             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42   
    610    None    None    None    None        None        None        None        None        None        None              1010            <NA>            9090   Reception            nan            0.48125            0.53704             <NA>             <NA>          3.48125          6.46296          2  University of Louisville  University of Dayton           17               42   
    611    None    None    None    None        None        None        None        None        None        None              1010            <NA>            9880   Reception            nan            0.48125            0.53704             <NA>             <NA>          3.10625         7.055552          2  University of Louisville  University of Dayton           17               42   
    612       7      25       9      11          10          15           8           5          16           3              <NA>            <NA>            <NA>   Reception            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42   
    613       7      25       9      11          10          15           8           5          16           3              <NA>            <NA>            <NA>   Reception            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42   
    614       7      25       9      11          10          15           8           5          16           3              <NA>            <NA>            <NA>       Serve            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42   
    615       7      25       9      11          10          15           8           5          16           3              <NA>            <NA>            <NA>       Serve            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42   
    616       7      25       9      11          10          15           8           5          16           3               220            <NA>            7957       Serve            nan            0.85625          -0.055552             <NA>             <NA>          2.24375         5.648146          2  University of Louisville  University of Dayton           17               42   
    617       7      25       9      11          10          15           8           5          16           3               220            <NA>            7957   Reception            nan            0.85625          -0.055552             <NA>             <NA>          2.24375         5.648146          2  University of Louisville  University of Dayton           17               42   

                     point_won_by              serving_team            receiving_team  rally_number  possesion_number  
    588  University of Louisville      University of Dayton  University of Louisville            11                 0  
    589  University of Louisville      University of Dayton  University of Louisville            11                 1  
    590  University of Louisville      University of Dayton  University of Louisville            11                 1  
    591  University of Louisville      University of Dayton  University of Louisville            11                 1  
    592  University of Louisville      University of Dayton  University of Louisville            11                 2  
    593  University of Louisville      University of Dayton  University of Louisville            11                 2  
    594  University of Louisville      University of Dayton  University of Louisville            11                 2  
    595  University of Louisville      University of Dayton  University of Louisville            11                 3  
    596  University of Louisville      University of Dayton  University of Louisville            11                 3  
    597  University of Louisville      University of Dayton  University of Louisville            11                 4  
    598  University of Louisville      University of Dayton  University of Louisville            11                 4  
    599  University of Louisville      University of Dayton  University of Louisville            11                 4  
    600  University of Louisville      University of Dayton  University of Louisville            11                 4  
    601  University of Louisville      University of Dayton  University of Louisville            11                 5  
    602  University of Louisville      University of Dayton  University of Louisville            11                 5  
    603  University of Louisville      University of Dayton  University of Louisville            11                 5  
    604  University of Louisville      University of Dayton  University of Louisville            11                 6  
    605  University of Louisville      University of Dayton  University of Louisville            11                 6  
    606  University of Louisville      University of Dayton  University of Louisville            11                 6  
    607  University of Louisville      University of Dayton  University of Louisville            11                 6  
    608  University of Louisville      University of Dayton  University of Louisville            11                 7  
    609  University of Louisville      University of Dayton  University of Louisville            11                 7  
    610      University of Dayton      University of Dayton  University of Louisville            11                 7  
    611      University of Dayton      University of Dayton  University of Louisville            11                 7  
    612      University of Dayton      University of Dayton  University of Louisville            11                 7  
    613      University of Dayton      University of Dayton  University of Louisville            11                 7  
    614      University of Dayton      University of Dayton  University of Louisville            11                 7  
    615      University of Dayton      University of Dayton  University of Louisville            11                 7  
    616      University of Dayton  University of Louisville      University of Dayton            12                 0  
    617      University of Dayton  University of Louisville      University of Dayton            12                 1  

------------------------------------------------------------------------

#### Reading multiple files - grouping for attacks and kills:

``` python
import pandas as pd
from datavolley import read_dv
import glob
import time

# Assign path
directory_path = "C:\\Users\\TylerWiddison\\Downloads\\"
file_extension = "*.dvw"
pattern = f"{directory_path}{file_extension}"

# Get a list of all files with the specified extension in the directory
file_list = glob.glob(pattern)

# Initialize an empty DataFrame to store combined data
combined_df = pd.DataFrame()

start_time = time.time()  # Record start time
# Loop through each file path
for path in file_list:
    dv_instance = read_dv.DataVolley(path)
    df = dv_instance.get_plays()

    # Concatenate the current DataFrame with the combined DataFrame
    combined_df = pd.concat([combined_df, df], ignore_index=True)

end_time = time.time()  # Record end time
processing_time = end_time - start_time
print(f"{len(file_list)} DVWs processed in {processing_time / 60:.2f} minutes")
# Filter for attacks and print attacks 
print(
    combined_df[combined_df['skill'] == 'Attack']
    .groupby(['player_name', 'team'])
    .agg(Att=('skill', 'count'),
         K=('evaluation_code', lambda x: x.eq('#').sum(skipna=True)),
         K_pct=('evaluation_code', lambda x: round((x.eq('#').sum(skipna=True) / x.count()), 3)))
    .reset_index()
    .sort_values(by='Att', ascending=False)
    .head(20)
    .reset_index(drop=True)
    .to_string()
)
```

    173 DVWs processed in 1.33 minutes
                player_name                         team   Att    K  K_pct
    0         Alexa Edwards    University of the Pacific  1004  371  0.370
    1   Grace Chillingworth        Pepperdine University   930  332  0.357
    2           Maui Robins       University of Portland   908  364  0.401
    3        Genevieve Bane         Saint Mary's College   859  257  0.299
    4         Maria Petkova  University of San Francisco   845  244  0.289
    5        Amber Stivrins      University of San Diego   827  285  0.345
    6      Biamba Kabengele    University of the Pacific   825  333  0.404
    7            Zoe Thiros           Gonzaga University   732  238  0.325
    8          Layla Truitt       Santa Clara University   713  235  0.330
    9        Kjersti Strong         Saint Mary's College   703  303  0.431
    10   Birdie Hendrickson        Pepperdine University   703  239  0.340
    11        Sophia Tulino       Santa Clara University   685  257  0.375
    12          Kylie Pries      University of San Diego   659  204  0.310
    13        Hannah Taylor         Saint Mary's College   657  246  0.374
    14           Lia Hawken       University of Portland   633  208  0.329
    15        Karolina Nova  University of San Francisco   625  181  0.290
    16     Kari Geissberger  Loyola Marymount University   624  266  0.426
    17         Elena Radeff       Santa Clara University   600  203  0.338
    18      Amethyst Harper  Loyola Marymount University   599  240  0.401
    19        Autumn Larson           Gonzaga University   598  146  0.244

------------------------------------------------------------------------

#### Reading multiple files parallel using threads:

``` python
import pandas as pd
from datavolley import read_dv
import glob
import time
import concurrent.futures

# Assign path
directory_path = "C:\\Users\\TylerWiddison\\Downloads\\"
file_extension = "*.dvw"
pattern = f"{directory_path}{file_extension}"

# Get a list of all files with the specified extension in the directory
file_list = glob.glob(pattern)

def read_file(file_path):
    dv_instance = read_dv.DataVolley(file_path)
    return dv_instance.get_plays()

def read_files_parallel(file_paths):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Use executor.map to parallelize file reading
        dfs = list(executor.map(read_file, file_paths))
    return pd.concat(dfs, ignore_index=True)

start_time = time.time()  # Record start time
if __name__ == "__main__":
    # Call the function to read files in parallel
    df = read_files_parallel(file_list)
    end_time = time.time()  # Record end time
    processing_time = end_time - start_time
    print(f"{len(file_list)} DVWs processed in {processing_time / 60:.2f} minutes")
    # Now 'df' contains the concatenated DataFrame from all files
    print(df.head())
```

    173 DVWs processed in 0.94 minutes
                                   match_id video_file_number video_time               code                  team player_number   player_name player_id  skill evaluation_code setter_position attack_code set_code set_type start_zone end_zone end_subzone num_players_numeric  home_team_score  visiting_team_score home_setter_position visiting_setter_position custom_code home_p1 home_p2 home_p3 home_p4  \
    0  df775e39-4ea5-4b08-a438-b52ecc03d79c                 1        464           *P05>LUp     Manhattan College           NaN           NaN       NaN    NaN             NaN               1         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             <NA>                 <NA>                    1                        1        None       5      14      11      17   
    1  df775e39-4ea5-4b08-a438-b52ecc03d79c                 1        464            *z1>LUp     Manhattan College           NaN           NaN       NaN    NaN             NaN               1         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             <NA>                 <NA>                    1                        1        None       5      14      11      17   
    2  df775e39-4ea5-4b08-a438-b52ecc03d79c                 1        464           aP18>LUp  Saint Mary's College           NaN           NaN       NaN    NaN             NaN               1         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             <NA>                 <NA>                    1                        1        None       5      14      11      17   
    3  df775e39-4ea5-4b08-a438-b52ecc03d79c                 1        464            az1>LUp  Saint Mary's College           NaN           NaN       NaN    NaN             NaN               1         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             <NA>                 <NA>                    1                        1        None       5      14      11      17   
    4  df775e39-4ea5-4b08-a438-b52ecc03d79c                 1        464  *05SM-~~~19D~~~00     Manhattan College             5  Sarah Emmons   -392555  Serve               -               1         NaN      NaN      NaN          1        9           D                 NaN                0                    1                    1                        1          00       5      14      11      17   

      home_p5 home_p6 visiting_p1 visiting_p2 visiting_p3 visiting_p4 visiting_p5 visiting_p6  start_coordinate  mid_coordinate  end_coordinate point_phase attack_phase start_coordinate_x start_coordinate_y mid_coordinate_x mid_coordinate_y end_coordinate_x end_coordinate_y set_number          home_team         visiting_team home_team_id visiting_team_id          point_won_by       serving_team  \
    0      10       9          18          24           5          14          25          21              <NA>            <NA>            <NA>   Reception          nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          1  Manhattan College  Saint Mary's College          179              359                   NaN                NaN   
    1      10       9          18          24           5          14          25          21              <NA>            <NA>            <NA>   Reception          nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          1  Manhattan College  Saint Mary's College          179              359                   NaN                NaN   
    2      10       9          18          24           5          14          25          21              <NA>            <NA>            <NA>   Reception          nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          1  Manhattan College  Saint Mary's College          179              359                   NaN                NaN   
    3      10       9          18          24           5          14          25          21              <NA>            <NA>            <NA>   Reception          nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          1  Manhattan College  Saint Mary's College          179              359                   NaN                NaN   
    4      10       9          18          24           5          14          25          21               476            <NA>            7131       Serve          nan            2.95625           0.092596             <NA>             <NA>          1.26875         5.055554          1  Manhattan College  Saint Mary's College          179              359  Saint Mary's College  Manhattan College   

             receiving_team  rally_number  possesion_number  
    0                   NaN             0                 0  
    1                   NaN             0                 1  
    2                   NaN             0                 1  
    3                   NaN             0                 1  
    4  Saint Mary's College             1                 0  

[^1]: If updating fails, you may need to `pip uninstall pydatavolley` -
    then reinstall `pip install pydatavolley`
