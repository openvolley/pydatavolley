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
pd.set_option('display.max_columns', 60)
pd.set_option('display.max_rows', 60)
pd.set_option('display.width', 280)
dv_instance = read_dv.DataVolley(None)
df = dv_instance.get_plays()
print(df[588:618])
```

                                     match_id video_file_number video_time                code                      team player_number      player_name player_id      skill evaluation_code setter_position attack_code set_code set_type start_zone end_zone end_subzone  \
    588  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2231   a10SM-~~~17A~~~+2      University of Dayton            10   Jamie Peterson    -11802      Serve               -               3         NaN      NaN      NaN          1        7           A   
    589  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2232  *10RM#~~~17AW~~-2F  University of Louisville            10      Mel McHenry    -75967  Reception               #               5         NaN      NaN      NaN          1        7           A   
    590  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2233   *19EQ#K1C~3B~~~-2  University of Louisville            19  Shannon Shields   -296094        Set               #               5         NaN       K1        C        NaN        3           B   
    591  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2234  *07AQ-X1~37AT2~-2F  University of Louisville             7      Emily Scott   -224837     Attack               -               5          X1      NaN      NaN          3        7           A   
    592  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2234  a02DQ+~~~37AS~~+2B      University of Dayton             2    Maura Collins   -230138        Dig               +               3         NaN      NaN      NaN          3        7           A   
    593  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2236   a08ET#K1F~8A~~~+2      University of Dayton             8  Brooke Westbeld   -232525        Set               #               3         NaN       K1        F        NaN        8           A   
    594  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2237  a05AT+X5~46CH2~+2F      University of Dayton             5      Alli Papesh   -230141     Attack               +               3          X5      NaN      NaN          4        6           C   
    595  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2238  *09DT-~~~46CS~~-2B  University of Louisville             9  Claire Chaussee   -225496        Dig               -               5         NaN      NaN      NaN          4        6           C   
    596  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2240  a15AO+~~~34BT1~+2F      University of Dayton            15     Rachael Fara   -273640     Attack               +               3         NaN      NaN      NaN          3        4           B   
    597  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2240  *10DO-~~~34BS~~-2F  University of Louisville            10      Mel McHenry    -75967        Dig               -               5         NaN      NaN      NaN          3        4           B   
    598  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2241  a03FH+~~~49C~~~+2B      University of Dayton             3  Elizabeth House   -230142   Freeball               +               3         NaN      NaN      NaN          4        9           C   
    599  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2243   a08EN#KBC~3D~~~+2      University of Dayton             8  Brooke Westbeld   -232525        Set               #               3         NaN       KB        C        NaN        3           D   
    600  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2244  a15AN-CF~28AP2~+2F      University of Dayton            15     Rachael Fara   -273640     Attack               -               3          CF      NaN      NaN          2        8           A   
    601  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2245  *19DN+~~~28AS~~-2B  University of Louisville            19  Shannon Shields   -296094        Dig               +               5         NaN      NaN      NaN          2        8           A   
    602  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2247   *08EH#~~~~7B~~~-2  University of Louisville             8    Lexi Hamilton    -75970        Set               #               5         NaN      NaN        ~        NaN        7           B   
    603  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2248  *10AH+V5~41CP2~-2F  University of Louisville            10      Mel McHenry    -75967     Attack               +               5          V5      NaN      NaN          4        1           C   
    604  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2249  a10DH-~~~41CS~~+2B      University of Dayton            10   Jamie Peterson    -11802        Dig               -               3         NaN      NaN      NaN          4        1           C   
    605  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2252  *09FH+~~~68B~~~-2B  University of Louisville             9  Claire Chaussee   -225496   Freeball               +               5         NaN      NaN      NaN          6        8           B   
    606  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2253   *19ET#K1B~2C~~~-2  University of Louisville            19  Shannon Shields   -296094        Set               #               5         NaN       K1        B        NaN        2           C   
    607  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2254  *15AT#X6~25CH4~-2F  University of Louisville            15       Aiko Jones   -224838     Attack               #               5          X6      NaN      NaN          2        5           C   
    608  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2254   a15BT=~~~~4C~~~+2      University of Dayton            15     Rachael Fara   -273640      Block               =               3         NaN      NaN      NaN        NaN        4           C   
    609  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2255             *p05:06  University of Louisville           NaN              NaN       NaN      Point             NaN               5         NaN      NaN      NaN        NaN      NaN         NaN   
    610  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2281             *c15:12  University of Louisville           NaN              NaN       NaN        NaN             NaN               0         NaN      NaN      NaN        NaN      NaN         NaN   
    611  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2281             *c19:25  University of Louisville           NaN              NaN       NaN        NaN             NaN               0         NaN      NaN      NaN        NaN      NaN         NaN   
    612  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2281                *P25  University of Louisville           NaN              NaN       NaN        NaN             NaN               4         NaN      NaN      NaN        NaN      NaN         NaN   
    613  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2281                 *z4  University of Louisville           NaN              NaN       NaN        NaN             NaN               4         NaN      NaN      NaN        NaN      NaN         NaN   
    614  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2281                aP08      University of Dayton           NaN              NaN       NaN        NaN             NaN               3         NaN      NaN      NaN        NaN      NaN         NaN   
    615  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2281                 az3      University of Dayton           NaN              NaN       NaN        NaN             NaN               3         NaN      NaN      NaN        NaN      NaN         NaN   
    616  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2281   *12SM+~~~56C~~~-1  University of Louisville            12      Tori Dilfer   -263069      Serve               +               4         NaN      NaN      NaN          5        6           C   
    617  773ce34e-1472-4a71-a691-7f7493b19f11                 1       2282  a03RM-~~~56CW~~+1B      University of Dayton             3  Elizabeth House   -230142  Reception               -               3         NaN      NaN      NaN          5        6           C   

        num_players_numeric  home_team_score  visiting_team_score home_setter_position visiting_setter_position custom_code home_p1 home_p2 home_p3 home_p4 home_p5 home_p6 visiting_p1 visiting_p2 visiting_p3 visiting_p4 visiting_p5 visiting_p6  start_coordinate  mid_coordinate  \
    588                 NaN                5                    6                    5                        3          +2      11      15      10       7      19       9          10          15           8           5          16           3               577            <NA>   
    589                 NaN                5                    6                    5                        3         -2F      11      15      10       7      19       9          10          15           8           5          16           3               577            <NA>   
    590                 NaN                5                    6                    5                        3          -2      11      15      10       7      19       9          10          15           8           5          16           3              4456            <NA>   
    591                   2                5                    6                    5                        3         -2F      11      15      10       7      19       9          10          15           8           5          16           3              4546            <NA>   
    592                 NaN                5                    6                    5                        3         +2B      11      15      10       7      19       9          10          15           8           5          16           3              4546            <NA>   
    593                 NaN                5                    6                    5                        3          +2      11      15      10       7      19       9          10          15           8           5          16           3              2959            <NA>   
    594                   2                5                    6                    5                        3         +2F      11      15      10       7      19       9          10          15           8           5          16           3              4315            <NA>   
    595                 NaN                5                    6                    5                        3         -2B      11      15      10       7      19       9          10          15           8           5          16           3              4315            <NA>   
    596                   1                5                    6                    5                        3         +2F      11      15      10       7      19       9          10          15           8           5          16           3              4550            <NA>   
    597                 NaN                5                    6                    5                        3         -2F      11      15      10       7      19       9          10          15           8           5          16           3              4550            <NA>   
    598                 NaN                5                    6                    5                        3         +2B      11      15      10       7      19       9          10          15           8           5          16           3              4528            <NA>   
    599                 NaN                5                    6                    5                        3          +2      11      15      10       7      19       9          10          15           8           5          16           3              4243            <NA>   
    600                   2                5                    6                    5                        3         +2F      11      15      10       7      19       9          10          15           8           5          16           3              4684            <NA>   
    601                 NaN                5                    6                    5                        3         -2B      11      15      10       7      19       9          10          15           8           5          16           3              4684            <NA>   
    602                 NaN                5                    6                    5                        3          -2      11      15      10       7      19       9          10          15           8           5          16           3              3230            <NA>   
    603                   2                5                    6                    5                        3         -2F      11      15      10       7      19       9          10          15           8           5          16           3              4321            <NA>   
    604                 NaN                5                    6                    5                        3         +2B      11      15      10       7      19       9          10          15           8           5          16           3              4321            <NA>   
    605                 NaN                5                    6                    5                        3         -2B      11      15      10       7      19       9          10          15           8           5          16           3              1857            <NA>   
    606                 NaN                5                    6                    5                        3          -2      11      15      10       7      19       9          10          15           8           5          16           3              4570            <NA>   
    607                   4                5                    6                    5                        3         -2F      11      15      10       7      19       9          10          15           8           5          16           3              4484            5484   
    608                 NaN                5                    6                    5                        3          +2      11      15      10       7      19       9          10          15           8           5          16           3              4616            <NA>   
    609                 NaN                5                    6                    5                        3        None      11      15      10       7      19       9          10          15           8           5          16           3              1807            <NA>   
    610                 NaN             <NA>                 <NA>                    0                        0        None      \n    None    None    None    None    None        None        None        None        None        None        None              1010            <NA>   
    611                 NaN             <NA>                 <NA>                    0                        0        None      \n    None    None    None    None    None        None        None        None        None        None        None              1010            <NA>   
    612                 NaN             <NA>                 <NA>                    4                        3        None      12      10       7      25       9      11          10          15           8           5          16           3              <NA>            <NA>   
    613                 NaN             <NA>                 <NA>                    4                        3        None      12      10       7      25       9      11          10          15           8           5          16           3              <NA>            <NA>   
    614                 NaN             <NA>                 <NA>                    4                        3        None      12      10       7      25       9      11          10          15           8           5          16           3              <NA>            <NA>   
    615                 NaN             <NA>                 <NA>                    4                        3        None      12      10       7      25       9      11          10          15           8           5          16           3              <NA>            <NA>   
    616                 NaN                5                    7                    4                        3          -1      12      10       7      25       9      11          10          15           8           5          16           3               220            <NA>   
    617                 NaN                5                    7                    4                        3         +1B      12      10       7      25       9      11          10          15           8           5          16           3               220            <NA>   

         end_coordinate point_phase   attack_phase start_coordinate_x start_coordinate_y mid_coordinate_x mid_coordinate_y end_coordinate_x end_coordinate_y set_number                 home_team         visiting_team home_team_id visiting_team_id              point_won_by  \
    588            7369       Serve            nan            2.99375            0.16667             <NA>             <NA>          2.69375         5.203702          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    589            7369   Reception            nan            2.99375            0.16667             <NA>             <NA>          2.69375         5.203702          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    590            <NA>   Reception            nan            2.20625           3.055556             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    591            7075   Reception      Reception            1.83125            3.12963             <NA>             <NA>          2.91875          4.98148          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    592            7075       Serve            nan            1.83125            3.12963             <NA>             <NA>          2.91875          4.98148          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    593            <NA>       Serve            nan            2.31875           1.944446             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    594            8150       Serve  BP-Transition            0.66875           2.981482             <NA>             <NA>          1.98125         5.796294          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    595            8150   Reception            nan            0.66875           2.981482             <NA>             <NA>          1.98125         5.796294          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    596            5572       Serve            nan            1.98125            3.12963             <NA>             <NA>          2.80625          3.87037          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    597            5572   Reception            nan            1.98125            3.12963             <NA>             <NA>          2.80625          3.87037          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    598            6827       Serve            nan            1.15625            3.12963             <NA>             <NA>          1.11875         4.833332          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    599            <NA>       Serve            nan            1.71875           2.907408             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    600            7043       Serve  BP-Transition            3.25625           3.203704             <NA>             <NA>          1.71875          4.98148          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    601            7043   Reception            nan            3.25625           3.203704             <NA>             <NA>          1.71875          4.98148          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    602            <NA>   Reception            nan            1.23125           2.166668             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    603            8127   Reception  SO-Transition            0.89375           2.981482             <NA>             <NA>          1.11875         5.796294          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    604            8127       Serve            nan            0.89375           2.981482             <NA>             <NA>          1.11875         5.796294          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    605            6742   Reception            nan            2.24375           1.129632             <NA>             <NA>          1.68125         4.759258          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    606            <NA>   Reception            nan            2.73125            3.12963             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    607            8084   Reception  SO-Transition            3.25625           3.055556          3.25625         3.796296          3.25625          5.72222          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    608            <NA>       Serve            nan            0.70625           3.203704             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    609            <NA>   Reception            nan            0.36875           1.129632             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42  University of Louisville   
    610            9090   Reception            nan            0.48125            0.53704             <NA>             <NA>          3.48125          6.46296          2  University of Louisville  University of Dayton           17               42      University of Dayton   
    611            9880   Reception            nan            0.48125            0.53704             <NA>             <NA>          3.10625         7.055552          2  University of Louisville  University of Dayton           17               42      University of Dayton   
    612            <NA>   Reception            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42      University of Dayton   
    613            <NA>   Reception            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42      University of Dayton   
    614            <NA>       Serve            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42      University of Dayton   
    615            <NA>       Serve            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          2  University of Louisville  University of Dayton           17               42      University of Dayton   
    616            7957       Serve            nan            0.85625          -0.055552             <NA>             <NA>          2.24375         5.648146          2  University of Louisville  University of Dayton           17               42      University of Dayton   
    617            7957   Reception            nan            0.85625          -0.055552             <NA>             <NA>          2.24375         5.648146          2  University of Louisville  University of Dayton           17               42      University of Dayton   

                     serving_team            receiving_team  rally_number  possesion_number  
    588      University of Dayton  University of Louisville            11                 0  
    589      University of Dayton  University of Louisville            11                 1  
    590      University of Dayton  University of Louisville            11                 1  
    591      University of Dayton  University of Louisville            11                 1  
    592      University of Dayton  University of Louisville            11                 2  
    593      University of Dayton  University of Louisville            11                 2  
    594      University of Dayton  University of Louisville            11                 2  
    595      University of Dayton  University of Louisville            11                 3  
    596      University of Dayton  University of Louisville            11                 3  
    597      University of Dayton  University of Louisville            11                 4  
    598      University of Dayton  University of Louisville            11                 4  
    599      University of Dayton  University of Louisville            11                 4  
    600      University of Dayton  University of Louisville            11                 4  
    601      University of Dayton  University of Louisville            11                 5  
    602      University of Dayton  University of Louisville            11                 5  
    603      University of Dayton  University of Louisville            11                 5  
    604      University of Dayton  University of Louisville            11                 6  
    605      University of Dayton  University of Louisville            11                 6  
    606      University of Dayton  University of Louisville            11                 6  
    607      University of Dayton  University of Louisville            11                 6  
    608      University of Dayton  University of Louisville            11                 7  
    609      University of Dayton  University of Louisville            11                 7  
    610      University of Dayton  University of Louisville            11                 7  
    611      University of Dayton  University of Louisville            11                 7  
    612      University of Dayton  University of Louisville            11                 7  
    613      University of Dayton  University of Louisville            11                 7  
    614      University of Dayton  University of Louisville            11                 7  
    615      University of Dayton  University of Louisville            11                 7  
    616  University of Louisville      University of Dayton            12                 0  
    617  University of Louisville      University of Dayton            12                 1  

------------------------------------------------------------------------

#### Reading multiple files - grouping for attacks and kills:

``` python
import pandas as pd
from datavolley import read_dv
import glob

directory_path = "C:\\Users\\TylerWiddison\\Downloads\\"
file_extension = "*.dvw"
pattern = f"{directory_path}{file_extension}"

# Get a list of all files with the specified extension in the directory
file_list = glob.glob(pattern)

# Initialize an empty DataFrame to store combined data
combined_df = pd.DataFrame()

# Loop through each file path
for path in file_list:
    dv_instance = read_dv.DataVolley(path)
    df = dv_instance.get_plays()

    # Concatenate the current DataFrame with the combined DataFrame
    combined_df = pd.concat([combined_df, df], ignore_index=True)

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

[^1]: If updating fails, you may need to `pip uninstall pydatavolley` -
    then reinstall `pip install pydatavolley`
