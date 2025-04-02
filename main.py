import pandas as pd

# Path to the CSV file
file_path = 'ufc-master.csv'

df1 = pd.read_csv(file_path)

file_path = 'data.csv'

df2 = pd.read_csv(file_path)


def rename_blue(col):
    if col.startswith("Blue"):
        new_col = col.replace("Blue", "B_", 1)
    else:
        new_col = col
    return new_col


def rename_red(col):
    if col.startswith("Red"):
        new_col = col.replace("Red", "R_", 1)
    else:
        new_col = col
    
    return new_col

def add_underscore(col):
    # Se la colonna inizia per 'R' o 'B'
    if col.startswith(('R', 'B')) and col != 'ReachDif' and col!='BetterRank':
        # Verifica che ci sia un secondo carattere e che non sia già un underscore
        if len(col) > 1 and col[1] != '_':
            return col[0] + '_' + col[1:]
    return col

df1 = df1.rename(columns=lambda x: rename_blue(x))
df1 = df1.rename(columns=lambda x: rename_red(x))
df1 = df1.rename(columns=lambda x: add_underscore(x))

def custom_normalize(col_name):
    # Converte l'intero nome in minuscolo
    col_name = col_name.lower()
    
    # Se la colonna inizia con 'r_' o 'b_', teniamo intatto 'r_'/'b_' e rimuoviamo i restanti underscore
    if col_name.startswith('r_') or col_name.startswith('b_'):
        prefix = col_name[:2]          # 'r_' o 'b_'
        rest = col_name[2:]           # il resto, es. 'height_cms'
        rest_no_underscores = rest.replace('_', '')  # 'heightcms'
        return prefix + rest_no_underscores          # 'r_heightcms'
    else:
        # Se non inizia con 'r_' o 'b_', togliamo tutti gli underscore
        return col_name.replace('_', '')

mapping_1_to_2 = {}
df1.columns = [col.lower() for col in df1.columns]
df2.columns = [col.lower() for col in df2.columns]

df1 = df1.rename(columns=lambda x: custom_normalize(x))
df2 = df2.rename(columns=lambda x: custom_normalize(x))

df2 = df2.rename(columns={'b_draw': 'b_draws', 'r_draw': 'r_draws','b_winbyko/tko':'b_winsbyko'
                          ,'r_winbyko/tko':'r_winsbyko', 'b_winbytkodoctorstoppage': 'b_winsbytkodoctorstoppage',
                          'r_winbytkodoctorstoppage': 'r_winsbytkodoctorstoppage',
                          'b_winbysubmission': 'b_winsbysubmission',
                          'r_winbysubmission': 'r_winsbysubmission',})



columns = list(sorted(set(df1.columns.tolist()).intersection(df2.columns.tolist())))

columns = [
    # -- FIGHT-LEVEL (data comune) --
    'r_fighter',
    'b_fighter',
    'date', 
    'location', 
    'winner', 
    'titlebout', 
    'weightclass',
    
    # -- B FIGHTER (dati generali) --
    
    'b_age',
    'b_stance',
    'b_heightcms',
    'b_reachcms',
    'b_weightlbs',

    # -- B FIGHTER (streak, record) --
    'b_currentlosestreak',
    'b_currentwinstreak',
    'b_draws',
    'b_longestwinstreak',
    'b_wins',
    'b_losses',
    'b_winsbyko',
    'b_winsbysubmission',
    'b_winsbytkodoctorstoppage',
    'b_totalroundsfought',
    'b_totaltitlebouts',

    # -- B FIGHTER (statistiche) --
    'b_avgsigstrlanded',
    'b_avgsigstrpct',
    'b_avgsubatt',
    'b_avgtdlanded',
    'b_avgtdpct',

    # -- R FIGHTER (dati generali) --
    
    'r_age',
    'r_stance',
    'r_heightcms',
    'r_reachcms',
    'r_weightlbs',

    # -- R FIGHTER (streak, record) --
    'r_currentlosestreak',
    'r_currentwinstreak',
    'r_draws',
    'r_longestwinstreak',
    'r_wins',
    'r_losses',
    'r_winsbyko',
    'r_winsbysubmission',
    'r_winsbytkodoctorstoppage',
    'r_totalroundsfought',
    'r_totaltitlebouts',

    # -- R FIGHTER (statistiche) --
    'r_avgsigstrlanded',
    'r_avgsigstrpct',
    'r_avgsubatt',
    'r_avgtdlanded',
    'r_avgtdpct'
]
df_final = pd.DataFrame()

df_final['RedFighter'] = df1['r_fighter']

ordered_cols = [
    # 1. Info generali evento
    'r_fighter','b_fighter','date', 'location', 'referee', 'winner', 'finish', 'finishdetails', 
    'finishround', 'finishroundtime', 'titlebout', 'weightclass', 'gender', 
    'numberofrounds', 'emptyarena', 'totalfighttimesecs', 'betterrank',

    # 2a. Blue Fighter (info generali)
     'b_age', 'b_stance', 'b_heightcms', 'b_reachcms', 'b_weightlbs', 
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
    'b_wflyweightrank', 'b_wstrawweightrank', 'b_welterweightrank',

    # 3a. Red Fighter (info generali)
     'r_age', 'r_stance', 'r_heightcms', 'r_reachcms', 'r_weightlbs',
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

    # 4. Differenze (gap Red vs. Blue)
    'agedif', 'avgsubattdif', 'avgtddif', 'heightdif', 'kodif', 'longestwinstreakdif',
    'losestreakdif', 'lossdif', 'reachdif', 'sigstrdif', 'subdif', 'totalrounddif',
    'totaltitleboutdif', 'windif', 'winstreakdif'
]

df1 = df1.sort_values(by=["date","r_fighter"]).reset_index(drop=True)
df2 = df2.sort_values(by=["date","r_fighter"]).reset_index(drop=True)

df1.drop(columns=('country'))

df = pd.DataFrame(columns=ordered_cols)

# Convertiamo tutte le colonne 'int' in float
for col in df1.select_dtypes(include='int'):
    df1[col] = df1[col].astype(float)


# Convertiamo tutte le colonne 'int' in float
for col in df2.select_dtypes(include='int'):
    df2[col] = df2[col].astype(float)

columns_to_update = [
    # Fight-level
    'location', 'winner', 'titlebout', 'weightclass',
    
    # B fighter (dati generali)
    'b_age','b_stance','b_heightcms','b_reachcms','b_weightlbs',

    # B fighter (streak, record)
    'b_currentlosestreak','b_currentwinstreak','b_draws','b_longestwinstreak','b_wins','b_losses',
    'b_winsbyko','b_winsbysubmission','b_winsbytkodoctorstoppage','b_totalroundsfought','b_totaltitlebouts',

    # B fighter (statistiche)
    'b_avgsigstrlanded','b_avgsigstrpct','b_avgsubatt','b_avgtdlanded','b_avgtdpct',

    # R fighter (dati generali)
    'r_age','r_stance','r_heightcms','r_reachcms','r_weightlbs',

    # R fighter (streak, record)
    'r_currentlosestreak','r_currentwinstreak','r_draws','r_longestwinstreak','r_wins','r_losses',
    'r_winsbyko','r_winsbysubmission','r_winsbytkodoctorstoppage','r_totalroundsfought','r_totaltitlebouts',

    # R fighter (statistiche)
    'r_avgsigstrlanded','r_avgsigstrpct','r_avgsubatt','r_avgtdlanded','r_avgtdpct'
]

# 1) Converti le date in datetime
df1['date'] = pd.to_datetime(df1['date'], errors='coerce')
df2['date'] = pd.to_datetime(df2['date'], errors='coerce')

# 2) (Opzionale) Filtra df1 sul range di date desiderato
start_date = '2010-03-21'
end_date   = '2021-03-20'
df1_sub = df1[(df1['date'] >= start_date) & (df1['date'] <= end_date)].copy()

# 3) Crea una colonna "pk" in df2 e df1_sub per avere una chiave univoca
df2['pk'] = (
    df2['date'].astype(str) + "_" +
    df2['r_fighter'].astype(str) + "_" +
    df2['b_fighter'].astype(str)
)

df1_sub['pk'] = (
    df1_sub['date'].astype(str) + "_" +
    df1_sub['r_fighter'].astype(str) + "_" +
    df1_sub['b_fighter'].astype(str)
)

# 4) Assegna i valori di df1_sub a df2.
#    Per ogni colonna, creiamo un dizionario {pk: valore_di_df1}, e lo mappiamo su df2.
#    In questo modo, df2[col] viene sovrascritto dai valori di df1_sub (anche se sono NaN).
for col in columns_to_update:
    if col in df1_sub.columns:
        # costruiamo la mappatura pk -> valore (df1_sub)
        map_dict = pd.Series(df1_sub[col].values, index=df1_sub['pk']).to_dict()
        # assegniamo a df2 i valori corrispondenti
        df2[col] = df2['pk'].map(map_dict)

# 5) Rimuoviamo la colonna pk da df2, se non serve più
df2.drop(columns='pk', inplace=True)

# A questo punto, df2 è stato "forzato" con i valori di df1_sub,
# sulle stesse righe (stessa chiave pk) e per le stesse date nel range


start_date = '2010-03-21'
end_date   = '2021-03-20'
df2 = df2[(df2['date'] >= start_date) & (df2['date'] <= end_date)].copy()
key_cols = ['r_fighter', 'b_fighter', 'date','winner'] 
df = pd.merge(df1, df2, how='outer', on=columns)
df = df.reindex(columns=ordered_cols)
df = df.sort_values(by=["date","r_fighter"]).reset_index(drop=True)
df.to_csv("df.csv",index = False)
df1[columns].to_csv('df1.csv',index = False)
df2[columns].to_csv('df2.csv',index = False)


#df.drop_duplicates(subset=['date','r_fighter'], keep='first', inplace=True)
#df.drop_duplicates(subset=['date','b_fighter'], keep='first', inplace=True)
df_duplicatesr = df[df.duplicated(subset=['date', 'r_fighter','b_fighter'], keep=False)]
df_duplicatesb = df[df.duplicated(subset=['date',  'b_fighter','b_fighter'], keep=False)]
cols= ['r_fighter', 'b_fighter','date']
df4 = df_duplicatesr[cols]
df5 = df_duplicatesb[cols]
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(df4,df5)