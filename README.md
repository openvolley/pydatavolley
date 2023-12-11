# pydatavolley

A python package for reading volleyball scouting files in DataVolley
format (\*.dvw).

### Installation

    pip install pydatavolley

### Example

Example file (using read_dv.DataVolley(None) will use example file) will
read if no path is provided:

``` python
from datavolley import read_dv

dv_instance = read_dv.DataVolley(None)
df = dv_instance.get_plays()
print(df.head(40))
```

                      code  point_phase attack_phase start_coordinate  \
    0             *P19>LUp          NaN          nan              NaN   
    1              *z1>LUp          NaN          nan              NaN   
    2             aP08>LUp          NaN          nan              NaN   
    3              az6>LUp          NaN          nan              NaN   
    4    *19SM+~~~78A~~~00          NaN          nan             0431   
    5   a02RM-~~~58AM~~00B          NaN          nan             0431   
    6    a08ET#~~~~8C~~~00          NaN          nan             3147   
    7   a10AT-X5~46CH2~00F          NaN    Reception             4512   
    8    *11BT+~~~~2C~~~00          NaN          nan             4578   
    9   *19DT+~~~42AB~~00B          NaN          nan             4512   
    10   *08EH#~~~~8A~~~00          NaN          nan             2859   
    11  *09AH#V5~41BH2~00F          NaN   Transition             4316   
    12   a17BH=~~~~2B~~~00          NaN          nan             4583   
    13             *p01:00          NaN          nan             4493   
    14                *P19          NaN          nan              NaN   
    15                 *z1          NaN          nan              NaN   
    16                aP08          NaN          nan              NaN   
    17                 az6          NaN          nan              NaN   
    18   *19SM#~~~71C~~~+1          NaN          nan             0529   
    19  a01RM=~~~51CM~~-1B          NaN          nan             0529   
    20             *p02:00          NaN          nan             4293   
    21                *P19          NaN          nan              NaN   
    22                 *z1          NaN          nan              NaN   
    23                aP08          NaN          nan              NaN   
    24                 az6          NaN          nan              NaN   
    25   *19SM-~~~71C~~~+2          NaN          nan             0526   
    26  a01RM+~~~51CR~~-2B          NaN          nan             0526   
    27   a08EQ#K1C~3A~~~-2          NaN          nan             4252   
    28  a16AQ=X1~31AH1~-2F          NaN    Reception             4444   
    29             *p03:00          NaN          nan             1187   
    30                *P19          NaN          nan              NaN   
    31                 *z1          NaN          nan              NaN   
    32                aP08          NaN          nan              NaN   
    33                 az6          NaN          nan              NaN   
    34   *19SM#~~~71B~~~+3          NaN          nan             0527   
    35  a01RM=~~~51BL~~-3B          NaN          nan             0527   
    36             *p04:00          NaN          nan             -113   
    37                *P19          NaN          nan              NaN   
    38                 *z1          NaN          nan              NaN   
    39                aP08          NaN          nan              NaN   

       mid_coordainte end_coordainte  time set home_setter_position  \
    0             NaN            NaN   NaN   1                    1   
    1             NaN            NaN   NaN   1                    1   
    2             NaN            NaN   NaN   1                    1   
    3             NaN            NaN   NaN   1                    1   
    4             NaN           7642   NaN   1                    1   
    5             NaN           7642   NaN   1                    1   
    6             NaN            NaN   NaN   1                    1   
    7            5522           8150   NaN   1                    1   
    8             NaN            NaN   NaN   1                    1   
    9            5522           5912   NaN   1                    1   
    10            NaN            NaN   NaN   1                    1   
    11           5517           7918   NaN   1                    1   
    12            NaN            NaN   NaN   1                    1   
    13            NaN            NaN   NaN   1                    1   
    14            NaN            NaN   NaN   1                    1   
    15            NaN            NaN   NaN   1                    1   
    16            NaN            NaN   NaN   1                    1   
    17            NaN            NaN   NaN   1                    1   
    18            NaN           7728   NaN   1                    1   
    19            NaN           7728   NaN   1                    1   
    20            NaN            NaN   NaN   1                    1   
    21            NaN            NaN   NaN   1                    1   
    22            NaN            NaN   NaN   1                    1   
    23            NaN            NaN   NaN   1                    1   
    24            NaN            NaN   NaN   1                    1   
    25            NaN           7728   NaN   1                    1   
    26            NaN           7728   NaN   1                    1   
    27            NaN            NaN   NaN   1                    1   
    28            NaN           8913   NaN   1                    1   
    29            NaN            NaN   NaN   1                    1   
    30            NaN            NaN   NaN   1                    1   
    31            NaN            NaN   NaN   1                    1   
    32            NaN            NaN   NaN   1                    1   
    33            NaN            NaN   NaN   1                    1   
    34            NaN           8017   NaN   1                    1   
    35            NaN           8017   NaN   1                    1   
    36            NaN            NaN   NaN   1                    1   
    37            NaN            NaN   NaN   1                    1   
    38            NaN            NaN   NaN   1                    1   
    39            NaN            NaN   NaN   1                    1   

       visiting_setter_position  ... visiting_team_id start_zone end_zone  \
    0                         6  ...               42        NaN      NaN   
    1                         6  ...               42        NaN      NaN   
    2                         6  ...               42        NaN      NaN   
    3                         6  ...               42        NaN      NaN   
    4                         6  ...               42          7        8   
    5                         6  ...               42          5        8   
    6                         6  ...               42        NaN        8   
    7                         6  ...               42          4        6   
    8                         6  ...               42        NaN        2   
    9                         6  ...               42          4        2   
    10                        6  ...               42        NaN        8   
    11                        6  ...               42          4        1   
    12                        6  ...               42        NaN        2   
    13                        6  ...               42        NaN      NaN   
    14                        6  ...               42        NaN      NaN   
    15                        6  ...               42        NaN      NaN   
    16                        6  ...               42        NaN      NaN   
    17                        6  ...               42        NaN      NaN   
    18                        6  ...               42          7        1   
    19                        6  ...               42          5        1   
    20                        6  ...               42        NaN      NaN   
    21                        6  ...               42        NaN      NaN   
    22                        6  ...               42        NaN      NaN   
    23                        6  ...               42        NaN      NaN   
    24                        6  ...               42        NaN      NaN   
    25                        6  ...               42          7        1   
    26                        6  ...               42          5        1   
    27                        6  ...               42        NaN        3   
    28                        6  ...               42          3        1   
    29                        6  ...               42        NaN      NaN   
    30                        6  ...               42        NaN      NaN   
    31                        6  ...               42        NaN      NaN   
    32                        6  ...               42        NaN      NaN   
    33                        6  ...               42        NaN      NaN   
    34                        6  ...               42          7        1   
    35                        6  ...               42          5        1   
    36                        6  ...               42        NaN      NaN   
    37                        6  ...               42        NaN      NaN   
    38                        6  ...               42        NaN      NaN   
    39                        6  ...               42        NaN      NaN   

       end_subzone rally_number              point_won_by home_team_score  \
    0          NaN            0                       NaN             NaN   
    1          NaN            0                       NaN             NaN   
    2          NaN            0                       NaN             NaN   
    3          NaN            0                       NaN             NaN   
    4            A            1  University of Louisville              01   
    5            A            1  University of Louisville              01   
    6            C            1  University of Louisville              01   
    7            C            1  University of Louisville              01   
    8            C            1  University of Louisville              01   
    9            A            1  University of Louisville              01   
    10           A            1  University of Louisville              01   
    11           B            1  University of Louisville              01   
    12           B            1  University of Louisville              01   
    13         NaN            1  University of Louisville              01   
    14         NaN            1  University of Louisville             NaN   
    15         NaN            1  University of Louisville             NaN   
    16         NaN            1  University of Louisville             NaN   
    17         NaN            1  University of Louisville             NaN   
    18           C            2  University of Louisville              02   
    19           C            2  University of Louisville              02   
    20         NaN            2  University of Louisville              02   
    21         NaN            2  University of Louisville             NaN   
    22         NaN            2  University of Louisville             NaN   
    23         NaN            2  University of Louisville             NaN   
    24         NaN            2  University of Louisville             NaN   
    25           C            3  University of Louisville              03   
    26           C            3  University of Louisville              03   
    27           A            3  University of Louisville              03   
    28           A            3  University of Louisville              03   
    29         NaN            3  University of Louisville              03   
    30         NaN            3  University of Louisville             NaN   
    31         NaN            3  University of Louisville             NaN   
    32         NaN            3  University of Louisville             NaN   
    33         NaN            3  University of Louisville             NaN   
    34           B            4  University of Louisville              04   
    35           B            4  University of Louisville              04   
    36         NaN            4  University of Louisville              04   
    37         NaN            4  University of Louisville             NaN   
    38         NaN            4  University of Louisville             NaN   
    39         NaN            4  University of Louisville             NaN   

       visiting_team_score              serving_team            receiving_team  
    0                  NaN                       NaN  University of Louisville  
    1                  NaN                       NaN  University of Louisville  
    2                  NaN                       NaN  University of Louisville  
    3                  NaN                       NaN  University of Louisville  
    4                   00  University of Louisville      University of Dayton  
    5                   00  University of Louisville      University of Dayton  
    6                   00  University of Louisville      University of Dayton  
    7                   00  University of Louisville      University of Dayton  
    8                   00  University of Louisville      University of Dayton  
    9                   00  University of Louisville      University of Dayton  
    10                  00  University of Louisville      University of Dayton  
    11                  00  University of Louisville      University of Dayton  
    12                  00  University of Louisville      University of Dayton  
    13                  00  University of Louisville      University of Dayton  
    14                 NaN  University of Louisville      University of Dayton  
    15                 NaN  University of Louisville      University of Dayton  
    16                 NaN  University of Louisville      University of Dayton  
    17                 NaN  University of Louisville      University of Dayton  
    18                  00  University of Louisville      University of Dayton  
    19                  00  University of Louisville      University of Dayton  
    20                  00  University of Louisville      University of Dayton  
    21                 NaN  University of Louisville      University of Dayton  
    22                 NaN  University of Louisville      University of Dayton  
    23                 NaN  University of Louisville      University of Dayton  
    24                 NaN  University of Louisville      University of Dayton  
    25                  00  University of Louisville      University of Dayton  
    26                  00  University of Louisville      University of Dayton  
    27                  00  University of Louisville      University of Dayton  
    28                  00  University of Louisville      University of Dayton  
    29                  00  University of Louisville      University of Dayton  
    30                 NaN  University of Louisville      University of Dayton  
    31                 NaN  University of Louisville      University of Dayton  
    32                 NaN  University of Louisville      University of Dayton  
    33                 NaN  University of Louisville      University of Dayton  
    34                  00  University of Louisville      University of Dayton  
    35                  00  University of Louisville      University of Dayton  
    36                  00  University of Louisville      University of Dayton  
    37                 NaN  University of Louisville      University of Dayton  
    38                 NaN  University of Louisville      University of Dayton  
    39                 NaN  University of Louisville      University of Dayton  

    [40 rows x 45 columns]
