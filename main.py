import pandas as pd

# Path to the CSV file
file_path = 'ufc-master.csv'

df = pd.read_csv(file_path)

columns = df.columns.tolist()
column_types = df.dtypes
column_nan = df.isna().any()

#Fight info
fight_info = ('RedFighter', 'BlueFighter','Date', 'Location', 'Country', 'Winner', 'TitleBout', 'WeightClass', 'Gender', 'NumberOfRounds',
              'LoseStreakDif', 'WinStreakDif', 'LongestWinStreakDif', 'WinDif', 'LossDif', 'TotalRoundDif', 'TotalTitleBoutDif', 'KODif',
              'SubDif', 'HeightDif', 'ReachDif', 'AgeDif', 'SigStrDif', 'AvgSubAttDif', 'AvgTDDif', 'EmptyArena','BetterRank', 'Finish',
              'FinishDetails', 'FinishRound', 'FinishRoundTime', 'TotalFightTimeSecs', 'RedOdds' ,'BlueOdds' ,'RedExpectedValue',
              'BlueExpectedValue','RedDecOdds', 'BlueDecOdds', 'RSubOdds', 'BSubOdds', 'RKOOdds', 'BKOOdds' )

#fighter info 
#primary key: Name + date
blue_fighter_col = ('BlueFighter','Gender','Date','BlueCurrentLoseStreak', 'BlueCurrentWinStreak', 'BlueDraws', 'BlueAvgSigStrLanded', 'BlueAvgSigStrPct', 
                    'BlueAvgSubAtt', 'BlueAvgTDLanded', 'BlueAvgTDPct', 'BlueLongestWinStreak', 'BlueLosses', 'BlueTotalRoundsFought', 
                    'BlueTotalTitleBouts', 'BlueWinsByDecisionMajority', 'BlueWinsByDecisionSplit', 'BlueWinsByDecisionUnanimous', 
                    'BlueWinsByKO', 'BlueWinsBySubmission', 'BlueWinsByTKODoctorStoppage', 'BlueWins', 'BlueStance','BlueHeightCms', 
                    'BlueReachCms', 'BlueWeightLbs','BlueAge','BMatchWCRank',  'BWFlyweightRank', 'BWFeatherweightRank', 'BWStrawweightRank', 
                    'BWBantamweightRank', 'BHeavyweightRank', 'BLightHeavyweightRank', 'BMiddleweightRank', 'BWelterweightRank', 
                    'BLightweightRank', 'BFeatherweightRank', 'BBantamweightRank', 'BFlyweightRank', 'BPFPRank')

red_fighter_col = ('RedFighter','Gender','Date','RedCurrentLoseStreak', 'RedCurrentWinStreak', 'RedDraws', 'RedAvgSigStrLanded', 'RedAvgSigStrPct', 
                   'RedAvgSubAtt', 'RedAvgTDLanded', 'RedAvgTDPct', 'RedLongestWinStreak', 'RedLosses', 'RedTotalRoundsFought', 
                   'RedTotalTitleBouts', 'RedWinsByDecisionMajority', 'RedWinsByDecisionSplit', 'RedWinsByDecisionUnanimous', 
                   'RedWinsByKO', 'RedWinsBySubmission', 'RedWinsByTKODoctorStoppage', 'RedWins', 'RedStance', 'RedHeightCms', 
                   'RedReachCms', 'RedWeightLbs', 'RedAge','RMatchWCRank', 'RWFlyweightRank', 'RWFeatherweightRank', 'RWStrawweightRank',
                    'RWBantamweightRank', 'RHeavyweightRank', 'RLightHeavyweightRank', 'RMiddleweightRank', 'RWelterweightRank', 
                    'RLightweightRank', 'RFeatherweightRank', 'RBantamweightRank', 'RFlyweightRank', 'RPFPRank')

df_fights = df[list(fight_info)]
df_blue_fighter = df[list(blue_fighter_col)]
df_red_fighter = df[list(red_fighter_col)]


def rename_blue(col):
    if col.startswith("Blue"):
        new_col = col.replace("Blue", "", 1)
    else:
        new_col = col
    if new_col == "Fighter":
        new_col = "Name"

    if new_col != "BantamweightRank":
        if new_col.startswith("B"):
            new_col = new_col.replace("B", "", 1)
    else:
        new_col = new_col
    return new_col


def rename_red(col):
    if col.startswith("Red"):
        new_col = col.replace("Red", "", 1)
    else:
        new_col = col
    if new_col == "Fighter":
        new_col = "Name"
    if new_col != "ReachCms":
        if new_col.startswith("R"):
            new_col = new_col.replace("R", "", 1)
        else:
            new_col = new_col
    return new_col


df_blue = df_blue_fighter.rename(columns=lambda x: rename_blue(x))
df_red = df_red_fighter.rename(columns=lambda x: rename_red(x))
df_fighters = pd.concat([df_red, df_blue], ignore_index=True)

df_fighters['Date'] = pd.to_datetime(df_fighters['Date'], errors='coerce')
df_fights = df_fights.copy()  # crea una copia indipendente
df_fights['Date'] = pd.to_datetime(df_fights['Date'], errors='coerce')
df_fighters = df_fighters.sort_values(by=["Name","Date"]).reset_index(drop=True)

df_fighters['WinsByDecision'] = df_fighters['WinsByDecisionMajority'] + df_fighters['WinsByDecisionSplit'] + df_fighters['WinsByDecisionUnanimous'] 
df_fighters['WinsByStoppage'] = df_fighters['WinsByKO'] + df_fighters['WinsBySubmission'] + df_fighters['WinsByTKODoctorStoppage']

df_fights_col = df_fights.columns.tolist()
df_fighters_col = df_fighters.columns.tolist()
df_fights_types = df_fights.dtypes
df_fighters_types = df_fighters.dtypes
df_fights_nan = df_fights.isna().any()
df_fighters_nan = df_fighters.isna().any()

df_fighters.to_csv("fighters.csv",index = False)
df_fights.to_csv("fights.csv",index = False)

print(df_fighters_col,'\n')
print(df_fights_col)


#decommentare se si vuole salvare in xlsx (ci mette 15 secondi)
#with pd.ExcelWriter("fighters.xlsx", engine='openpyxl') as writer:
   # df_fighters.to_excel(writer, index=False)


#with pd.ExcelWriter("fights.xlsx", engine='openpyxl') as writer:
    #df_fights.to_excel(writer, index=False)