# pydatavolley

A python package for reading volleyball scouting files in DataVolley
format (\*.dvw).

Work in progress.

### Installation

    pip install pydatavolley
    pip install --upgrade pydatavolley

## <u>Examples</u>

Example file (using read_dv.DataVolley(None) will use example file) will
read if no path is provided OR reading one file:

#### Reading one file:

``` python
import pandas as pd
from datavolley import read_dv
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 280)
dv_instance = read_dv.DataVolley(None)
df = dv_instance.get_plays()
print('Attacks filtered\n' + df.head(20).to_string())
```

    Attacks filtered
                                    match_id video_file_number video_time                code                      team player_number         player_name player_id      skill evaluation_code setter_position attack_code set_code set_type start_zone end_zone end_subzone num_players_numeric home_team_score visiting_team_score home_setter_position visiting_setter_position custom_code home_p1 home_p2 home_p3 home_p4 home_p5 home_p6 visiting_p1 visiting_p2 visiting_p3 visiting_p4 visiting_p5 visiting_p6  start_coordinate  mid_coordinate  end_coordinate point_phase   attack_phase start_coordinate_x start_coordinate_y mid_coordinate_x mid_coordinate_y end_coordinate_x end_coordinate_y set_number                 home_team         visiting_team home_team_id visiting_team_id              point_won_by              serving_team        receiving_team  rally_number custom_code  possesion_number
    0   d7f3a629-13fb-427e-80d1-fb23099d8441                 1        494            *P19>LUp  University of Louisville           NaN                 NaN       NaN        NaN             NaN               1         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             NaN                 NaN                    1                        6                  19       9      11      15      10       7           1          16          17          10           6           8              <NA>            <NA>            <NA>   Reception            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          1  University of Louisville  University of Dayton           17               42                       NaN                       NaN                   NaN             0                             0
    1   d7f3a629-13fb-427e-80d1-fb23099d8441                 1        494             *z1>LUp  University of Louisville           NaN                 NaN       NaN        NaN             NaN               1         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             NaN                 NaN                    1                        6                  19       9      11      15      10       7           1          16          17          10           6           8              <NA>            <NA>            <NA>   Reception            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          1  University of Louisville  University of Dayton           17               42                       NaN                       NaN                   NaN             0                             1
    2   d7f3a629-13fb-427e-80d1-fb23099d8441                 1        494            aP08>LUp      University of Dayton           NaN                 NaN       NaN        NaN             NaN               6         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             NaN                 NaN                    1                        6                  19       9      11      15      10       7           1          16          17          10           6           8              <NA>            <NA>            <NA>   Reception            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          1  University of Louisville  University of Dayton           17               42                       NaN                       NaN                   NaN             0                             1
    3   d7f3a629-13fb-427e-80d1-fb23099d8441                 1        494             az6>LUp      University of Dayton           NaN                 NaN       NaN        NaN             NaN               6         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             NaN                 NaN                    1                        6                  19       9      11      15      10       7           1          16          17          10           6           8              <NA>            <NA>            <NA>   Reception            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          1  University of Louisville  University of Dayton           17               42                       NaN                       NaN                   NaN             0                             1
    4   d7f3a629-13fb-427e-80d1-fb23099d8441                 1        494   *19SM+~~~78A~~~00  University of Louisville            19     Shannon Shields   -296094      Serve               +               1         NaN      NaN      NaN          7        8           A                 NaN              01                  00                    1                        6          00      19       9      11      15      10       7           1          16          17          10           6           8               431            <NA>            7642       Serve            nan            1.26875           0.092596             <NA>             <NA>          1.68125         5.425924          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             1          00                 0
    5   d7f3a629-13fb-427e-80d1-fb23099d8441                 1        495  a02RM-~~~58AM~~00B      University of Dayton             2       Maura Collins   -230138  Reception               -               6         NaN      NaN      NaN          5        8           A                 NaN              01                  00                    1                        6         00B      19       9      11      15      10       7           1          16          17          10           6           8               431            <NA>            7642   Reception            nan            1.26875           0.092596             <NA>             <NA>          1.68125         5.425924          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             1         00B                 1
    6   d7f3a629-13fb-427e-80d1-fb23099d8441                 1        497   a08ET#~~~~8C~~~00      University of Dayton             8     Brooke Westbeld   -232525        Set               #               6         NaN      NaN        ~        NaN        8           C                 NaN              01                  00                    1                        6          00      19       9      11      15      10       7           1          16          17          10           6           8              3147            <NA>            <NA>   Reception            nan            1.86875           2.092594             <NA>             <NA>             <NA>             <NA>          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             1          00                 1
    7   d7f3a629-13fb-427e-80d1-fb23099d8441                 1        499  a10AT-X5~46CH2~00F      University of Dayton            10      Jamie Peterson    -11802     Attack               -               6          X5      NaN      NaN          4        6           C                   2              01                  00                    1                        6                  19       9      11      15      10       7           1          16          17          10           6           8              4512            5522            8150   Reception      Reception            0.55625            3.12963          0.93125          3.87037          1.98125         5.796294          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             1                             1
    8   d7f3a629-13fb-427e-80d1-fb23099d8441                 1        499   *11BT+~~~~2C~~~00  University of Louisville            11      Anna Stevenson   -278838      Block               +               1         NaN      NaN      NaN        NaN        2           C                 NaN              01                  00                    1                        6          00      19       9      11      15      10       7           1          16          17          10           6           8              4578            <NA>            <NA>       Serve            nan            3.03125            3.12963             <NA>             <NA>             <NA>             <NA>          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             1          00                 2
    9   d7f3a629-13fb-427e-80d1-fb23099d8441                 1        500  *19DT+~~~42AB~~00B  University of Louisville            19     Shannon Shields   -296094        Dig               +               1         NaN      NaN      NaN          4        2           A                 NaN              01                  00                    1                        6         00B      19       9      11      15      10       7           1          16          17          10           6           8              4512            5522            5912       Serve            nan            0.55625            3.12963          0.93125          3.87037          0.55625         4.166666          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             1         00B                 2
    10  d7f3a629-13fb-427e-80d1-fb23099d8441                 1        502   *08EH#~~~~8A~~~00  University of Louisville             8       Lexi Hamilton    -75970        Set               #               1         NaN      NaN        ~        NaN        8           A                 NaN              01                  00                    1                        6          00      19       9      11      15      10       7           1          16          17          10           6           8              2859            <NA>            <NA>       Serve            nan            2.31875           1.870372             <NA>             <NA>             <NA>             <NA>          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             1          00                 2
    11  d7f3a629-13fb-427e-80d1-fb23099d8441                 1        504  *09AH#V5~41BH2~00F  University of Louisville             9     Claire Chaussee   -225496     Attack               #               1          V5      NaN      NaN          4        1           B                   2              01                  00                    1                        6                  19       9      11      15      10       7           1          16          17          10           6           8              4316            5517            7918       Serve  BP-Transition            0.70625           2.981482          0.74375          3.87037          0.78125         5.648146          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             1                             2
    12  d7f3a629-13fb-427e-80d1-fb23099d8441                 1        504   a17BH=~~~~2B~~~00      University of Dayton            17          Sierra Pla    -11804      Block               =               6         NaN      NaN      NaN        NaN        2           B                 NaN              01                  00                    1                        6          00      19       9      11      15      10       7           1          16          17          10           6           8              4583            <NA>            <NA>   Reception            nan            3.21875            3.12963             <NA>             <NA>             <NA>             <NA>          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             1          00                 3
    13  d7f3a629-13fb-427e-80d1-fb23099d8441                 1        504             *p01:00  University of Louisville           NaN                 NaN       NaN      Point             NaN               1         NaN      NaN      NaN        NaN      NaN         NaN                 NaN              01                  00                    1                        6                  19       9      11      15      10       7           1          16          17          10           6           8              4493            <NA>            <NA>       Serve            nan            3.59375           3.055556             <NA>             <NA>             <NA>             <NA>          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             1                             3
    14  d7f3a629-13fb-427e-80d1-fb23099d8441                 1        519                *P19  University of Louisville           NaN                 NaN       NaN        NaN             NaN               1         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             NaN                 NaN                    1                        6                  19       9      11      15      10       7           1          16          17          10           6           8              <NA>            <NA>            <NA>       Serve            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             1                             3
    15  d7f3a629-13fb-427e-80d1-fb23099d8441                 1        519                 *z1  University of Louisville           NaN                 NaN       NaN        NaN             NaN               1         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             NaN                 NaN                    1                        6                  19       9      11      15      10       7           1          16          17          10           6           8              <NA>            <NA>            <NA>       Serve            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             1                             3
    16  d7f3a629-13fb-427e-80d1-fb23099d8441                 1        519                aP08      University of Dayton           NaN                 NaN       NaN        NaN             NaN               6         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             NaN                 NaN                    1                        6                  19       9      11      15      10       7           1          16          17          10           6           8              <NA>            <NA>            <NA>   Reception            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             1                             3
    17  d7f3a629-13fb-427e-80d1-fb23099d8441                 1        519                 az6      University of Dayton           NaN                 NaN       NaN        NaN             NaN               6         NaN      NaN      NaN        NaN      NaN         NaN                 NaN             NaN                 NaN                    1                        6                  19       9      11      15      10       7           1          16          17          10           6           8              <NA>            <NA>            <NA>   Reception            nan               <NA>               <NA>             <NA>             <NA>             <NA>             <NA>          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             1                             3
    18  d7f3a629-13fb-427e-80d1-fb23099d8441                 1        519   *19SM#~~~71C~~~+1  University of Louisville            19     Shannon Shields   -296094      Serve               #               1         NaN      NaN      NaN          7        1           C                 NaN              02                  00                    1                        6          +1      19       9      11      15      10       7           1          16          17          10           6           8               529            <NA>            7728       Serve            nan            1.19375            0.16667             <NA>             <NA>          1.15625         5.499998          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             2          +1                 0
    19  d7f3a629-13fb-427e-80d1-fb23099d8441                 1        521  a01RM=~~~51CM~~-1B      University of Dayton             1  Mikaylah Van Lanen   -231069  Reception               =               6         NaN      NaN      NaN          5        1           C                 NaN              02                  00                    1                        6         -1B      19       9      11      15      10       7           1          16          17          10           6           8               529            <NA>            7728   Reception            nan            1.19375            0.16667             <NA>             <NA>          1.15625         5.499998          1  University of Louisville  University of Dayton           17               42  University of Louisville  University of Louisville  University of Dayton             2         -1B                 1

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


filtered_df = combined_df[combined_df['skill'] == 'Attack']
print(
    'Attacks filtered\n' + '\n' + filtered_df.groupby(['player_name', 'team'])
    .agg(at=('skill', 'count'),
         k=('evaluation_code', lambda x: x.eq('#').sum(skipna=True)),
         k_pct=('evaluation_code', lambda x: round((x.eq('#').sum(skipna=True) / x.count()), 3)))
    .reset_index()
    .sort_values(by='at', ascending=False)
    .head(20)
    .reset_index(drop=True)
    .to_string()
)
```

    Attacks filtered

                player_name                         team    at    k  k_pct
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
