import pandas as pd

# Path to the CSV file
file_path = 'df.csv'

df = pd.read_csv(file_path)

columns = df.columns.tolist()
column_types = df.dtypes
column_nan = df.isna().any()

fights_col = ['r_fighter','b_fighter','date', 'location', 'referee', 'winner', 'finish', 'finishdetails', 
    'finishround', 'finishroundtime', 'titlebout', 'weightclass', 'gender', 
    'numberofrounds', 'emptyarena', 'totalfighttimesecs', 'betterrank','agedif', 'avgsubattdif', 'avgtddif', 
    'heightdif', 'kodif', 'longestwinstreakdif',
    'losestreakdif', 'lossdif', 'reachdif', 'sigstrdif', 'subdif', 'totalrounddif',
    'totaltitleboutdif', 'windif', 'winstreakdif'
]


r_fighters_col = [
    # 3a. Red Fighter (info generali)
    'r_fighter', 'date','r_age' ,'r_stance', 'r_heightcms', 'r_reachcms', 'r_weightlbs',
    'r_odds', 'r_decodds', 'r_subodds', 'r_koodds', 'r_expectedvalue',

    # 3b. Red Fighter (streak)
    'r_currentwinstreak', 'r_currentlosestreak', 'r_longestwinstreak', 'r_losses',
    'r_draws', 'r_wins',

    # 3c. Red Fighter (tipi di vittoria)
    'r_winbydecisionmajority', 'r_winbydecisionsplit', 'r_winbydecisionunanimous', 
    'r_winsbydecisionmajority', 'r_winsbydecisionsplit', 'r_winsbydecisionunanimous',
    'r_winsbyko', 'r_winsbysubmission', 'r_winsbytkodoctorstoppage',

    # 3d. Red Fighter (statistiche avanzate)
    'r_avgkd', 'r_avgoppkd', 'r_avgsigstratt', 'r_avgsigstrlanded', 'r_avgsigstrpct',
    'r_avgoppsigstratt', 'r_avgoppsigstrlanded', 'r_avgoppsigstrpct',
    'r_avgtdatt', 'r_avgtdlanded', 'r_avgtdpct', 'r_avgopptdatt', 'r_avgopptdlanded',
    'r_avgopptdpct', 'r_avgsubatt', 'r_avgoppsubatt', 'r_avgrev', 'r_avgopprev',
    'r_avgheadatt', 'r_avgheadlanded', 'r_avgoppheadatt', 'r_avgoppheadlanded',
    'r_avgbodyatt', 'r_avgbodylanded', 'r_avgoppbodyatt', 'r_avgoppbodylanded',
    'r_avglegatt', 'r_avgleglanded', 'r_avgopplegatt', 'r_avgoppleglanded',
    'r_avgdistanceatt', 'r_avgdistancelanded', 'r_avgoppdistanceatt', 'r_avgoppdistancelanded',
    'r_avgclinchatt', 'r_avgclinchlanded', 'r_avgoppclinchatt', 'r_avgoppclinchlanded',
    'r_avggroundatt', 'r_avggroundlanded', 'r_avgoppgroundatt', 'r_avgoppgroundlanded',
    'r_avgctrltime(seconds)', 'r_avgoppctrltime(seconds)',

    # 3e. Red Fighter (tempo e round)
    'r_totaltimefought(seconds)', 'r_totalroundsfought', 'r_totaltitlebouts',

    # 3f. Red Fighter (rank ecc.)
    'r_matchwcrank', 'r_bantamweightrank', 'r_featherweightrank', 'r_flyweightrank',
    'r_heavyweightrank', 'r_lightheavyweightrank', 'r_lightweightrank',
    'r_middleweightrank', 'r_pfprank', 'r_wbantamweightrank', 'r_wfeatherweightrank',
    'r_wflyweightrank', 'r_wstrawweightrank', 'r_welterweightrank',
]

b_fighters_col = [
    'b_fighter','date', 'b_age', 'b_stance', 'b_heightcms', 'b_reachcms', 'b_weightlbs', 
    'b_odds', 'b_decodds', 'b_subodds', 'b_koodds', 'b_expectedvalue',

    # 2b. Blue Fighter (streak)
    'b_currentwinstreak', 'b_currentlosestreak', 'b_longestwinstreak', 'b_losses', 
    'b_draws', 'b_wins',

    # 2c. Blue Fighter (tipi di vittoria)
    'b_winbydecisionmajority', 'b_winbydecisionsplit', 'b_winbydecisionunanimous', 
    'b_winsbydecisionmajority', 'b_winsbydecisionsplit', 'b_winsbydecisionunanimous', 
    'b_winsbyko', 'b_winsbysubmission', 'b_winsbytkodoctorstoppage',

    # 2d. Blue Fighter (statistiche avanzate)
    'b_avgkd', 'b_avgoppkd', 'b_avgsigstratt', 'b_avgsigstrlanded', 'b_avgsigstrpct',
    'b_avgoppsigstratt', 'b_avgoppsigstrlanded', 'b_avgoppsigstrpct',
    'b_avgtdatt', 'b_avgtdlanded', 'b_avgtdpct', 'b_avgopptdatt', 'b_avgopptdlanded',
    'b_avgopptdpct', 'b_avgsubatt', 'b_avgoppsubatt', 'b_avgrev', 'b_avgopprev',
    'b_avgheadatt', 'b_avgheadlanded', 'b_avgoppheadatt', 'b_avgoppheadlanded',
    'b_avgbodyatt', 'b_avgbodylanded', 'b_avgoppbodyatt', 'b_avgoppbodylanded',
    'b_avglegatt', 'b_avgleglanded', 'b_avgopplegatt', 'b_avgoppleglanded',
    'b_avgdistanceatt', 'b_avgdistancelanded', 'b_avgoppdistanceatt', 'b_avgoppdistancelanded',
    'b_avgclinchatt', 'b_avgclinchlanded', 'b_avgoppclinchatt', 'b_avgoppclinchlanded',
    'b_avggroundatt', 'b_avggroundlanded', 'b_avgoppgroundatt', 'b_avgoppgroundlanded',
    'b_avgctrltime(seconds)', 'b_avgoppctrltime(seconds)',

    # 2e. Blue Fighter (tempo e round)
    'b_totaltimefought(seconds)', 'b_totalroundsfought', 'b_totaltitlebouts',

    # 2f. Blue Fighter (rank ecc.)
    'b_matchwcrank', 'b_bantamweightrank', 'b_featherweightrank', 'b_flyweightrank',
    'b_heavyweightrank', 'b_lightheavyweightrank', 'b_lightweightrank', 
    'b_middleweightrank', 'b_pfprank', 'b_wbantamweightrank', 'b_wfeatherweightrank',
    'b_wflyweightrank', 'b_wstrawweightrank', 'b_welterweightrank'
]

df_fights = df[list(fights_col)]
df_blue_fighter = df[list(b_fighters_col)]
df_red_fighter = df[list(r_fighters_col)]


def rename_blue(col):
    if col.startswith("b_"):
        new_col = col.replace("b_", "", 1)
    else:
        new_col = col
    return new_col


def rename_red(col):
    if col.startswith("r_"):
        new_col = col.replace("r_", "", 1)
    else:
        new_col = col
    return new_col

df_blue = df_blue_fighter.rename(columns=lambda x: rename_blue(x))
df_red = df_red_fighter.rename(columns=lambda x: rename_red(x))
df_fighters = pd.concat([df_red, df_blue], ignore_index=True)

df_fighters = df_fighters.sort_values(by=["fighter","date"]).reset_index(drop=True)

df_fighters['winsbydecision'] = df_fighters['winsbydecisionmajority'] + df_fighters['winsbydecisionsplit'] + df_fighters['winsbydecisionunanimous']
df_fighters['winsbystoppage'] = df_fighters['winsbyko'] + df_fighters['winsbysubmission'] + df_fighters['winsbytkodoctorstoppage']

df_fighters.to_csv("fighters.csv",index = False)
df_fights.to_csv("fights.csv",index = False)


