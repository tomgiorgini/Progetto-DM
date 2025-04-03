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

df = pd.DataFrame(columns=ordered_cols)

df1 = df1.sort_values(by=["date","r_fighter"]).reset_index(drop=True)
df2 = df2.sort_values(by=["date","r_fighter"]).reset_index(drop=True)

df1.drop(columns=('country'))

# Convertiamo tutte le colonne 'int' in float
for col in df1.select_dtypes(include='int'):
    df1[col] = df1[col].astype(float)
    
for col in df1.select_dtypes(include='object'):
    df1[col] = df1[col].fillna('').astype(str)
for col in df2.select_dtypes(include='object'):
    df2[col] = df2[col].fillna('').astype(str)
    
df1 = df1.round(2)
df2 = df2.round(2)

name_map = {
    "Quinton Jackson": "Rampage Jackson",
    "Mirko Cro Cop": "Mirko Filipovic",
    "Antonio Rodrigo Nogueira": "Minotauro Nogueira",
    "Tiequan Zhang": "Zhang Tiequan",
    "Constantinos Philippou": "Costas Philippou",
    "Ben Alloway": "Benny Alloway",
    "Bubba McDaniel": "Robert McDaniel",
    "William Macario": "William Patolino",
    "Brad Scott": "Bradley Scott",
    "Rafael Cavalcante": "Rafael Feijao",
    "Josh Sampo": "Joshua Sampo",
    "Junior Hernandez": "Ramiro Hernandez",
    "Edimilson Souza": "Kevin Souza",
    "An Ying Wang": "Anying Wang",
    "Guangyou Ning": "Ning Guangyou",
    "Nicholas Musoke": "Nico Musoke",
    "Juan Manuel Puig": "Juan Puig",
    "Emily Kagan": "Emily Peters Kagan",
    "Tiago Trator": "Tiago dos Santos e Silva",
    "Roldan Sangcha'an": "Roldan Sangcha-an",
    "Wendell Oliveira": "Wendell Oliveira Marques",
    "Rob Whiteford": "Robert Whiteford",
    "Glaico Franca": "Glaico Franca Moreira",
    "Bruno Korea": "Bruno Rodrigues",
    "Seo Hee Ham": "Seohee Ham",
    "Tim Johnson": "Timothy Johnson",
    "Joe Gigliotti": "Joseph Gigliotti",
    "Alvaro Herrera": "Alvaro Herrera Mendoza",
    "Cris Cyborg": "Cristiane Justino",
    "Marco Polo Reyes": "Polo Reyes",
    "Ulka Sasaki": "Yuta Sasaki",
    "Da Un Jung": "Da-Un Jung",
    "Caludio Puelles": "Claudio Puelles",
    "Raphael Pessoa": "Raphael Pessoa Nunes",
    "Alekander Volkov": "Alexander Volkov",
    "Grigorii Popov": "Grigory Popov",
    "Peter Yan": "Petr Yan",
    "Jun Yong Park": "Junyong Park",
    "SeungWoo Choi": "Seungwoo Choi",
    "Jim Crute": "Jimmy Crute",
    "Kai Kara France": "Kai Kara-France",
    "Batgerel Danaa": "Danaa Batgerel",
    "Weili Zhang": "Zhang Weili",
    "Elizeu Dos Santos": "Elizeu Zaleski dos Santos",
    "Bibulatov Magomed": "Magomed Bibulatov",
    "Aleksandra Albu": "Alexandra Albu",
    "Caludia Gadelha": "Claudia Gadelha",
    "Germaine De Randamie": "Germaine de Randamie",
    "Eduardo Garagorri": "Luiz Garagorri",
    "Vicente Luque": "Vincente Luque",
    "Vernon Ramos": "Vernon Ramos Ho",
    "Robert Sanchez": "Roberto Sanchez",
    "Liu Pingyuan": "Pingyuan Liu",
    "Jun Yong Park": "Junyong Park",
    "Rodolfo Rubio": "Rodolfo Rubio Perez",
    "Humberto Brown": "Humberto Brown Morrison",
    "Heather Clark": "Heather Jo Clark",
    "Leonardo Augusto Leleco": "Leonardo Guimaraes",
    "Alessandro Ricci": "Alex Ricci",
    "Jim Wallhead": "Jimmy Wallhead",
    "Chan-Mi Jeon": "Chanmi Jeon",
    "Azunna Anyanwu": "Zu Anyanwu",
    "Carlo Pedersoli": "Carlo Pedersoli Jr.",
    "Anthony Rocco Martin": "Rocco Martin",
    "Krzystof Jotko": "Krzysztof Jotko",
    "Derrick": "Derrick Krantz",
    "Inoue Mizuki": "Mizuki Inoue",
    "Don'Tale Mayes": "Don'tale Mayes",
    "Isabela De Pauda": "Isabela de Padua",
    "Omar Antonio Morales Ferrer": "Omar Morales",
    "Ode Obsourne": "Ode Osbourne",
    "Luci Pudilova": "Lucie Pudilova",
    "Kalinn Williams": "Khaos Williams",
    "Youssef Zalal": "Youssef Zalel",
    "Marcos Rogerio De Lima": "Marcos Rogerio de Lima",
    "Josh Culibao": "Joshua Culibao",
    "Zhalgas Zhamagulov": "Zhalgas Zhumagulov",
    "Ali AlQaisi": "Ali Qaisi",
    "Alex Munoz": "Alexander Munoz",
    "Phil Hawes": "Phillip Hawes"
}

df1['r_fighter'] = df1['r_fighter'].replace(name_map)
df1['b_fighter'] = df1['b_fighter'].replace(name_map)
df2['b_fighter'] = df2['b_fighter'].replace(name_map)
df2['r_fighter'] = df2['r_fighter'].replace(name_map)


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
#start_date = '2010-03-21'
#end_date   = '2021-03-20'
#df2 = df2[(df2['date'] >= start_date) & (df2['date'] <= end_date)].copy()
#df1 = df1[(df1['date'] >= start_date) & (df1['date'] <= end_date)].copy()

# 3) Crea una colonna "pk" in df2 e df1_sub per avere una chiave univoca
df2['pk'] = (
    df2['date'].astype(str) + "_" +
    df2['r_fighter'].astype(str) + "_" +
    df2['b_fighter'].astype(str)
)

df1['pk'] = (
    df1['date'].astype(str) + "_" +
    df1['r_fighter'].astype(str) + "_" +
    df1['b_fighter'].astype(str)
)

# 4) Assegna i valori di df1_sub a df2.
#    Per ogni colonna, creiamo un dizionario {pk: valore_di_df1}, e lo mappiamo su df2.
#    In questo modo, df2[col] viene sovrascritto dai valori di df1_sub (anche se sono NaN).
for col in columns_to_update:
    if col in df1.columns:
        # costruiamo la mappatura pk -> valore (df1_sub)
        map_dict = pd.Series(df1[col].values, index=df1['pk']).to_dict()
        # assegniamo a df2 i valori corrispondenti
        df2[col] = df2['pk'].map(map_dict)

# 5) Rimuoviamo la colonna pk da df2, se non serve più
df2.drop(columns='pk', inplace=True)

# A questo punto, df2 è stato "forzato" con i valori di df1_sub,
# sulle stesse righe (stessa chiave pk) e per le stesse date nel range



key_cols = ['r_fighter', 'b_fighter', 'date'] 
df = pd.merge(df1, df2, how='outer', on=columns)
df = df.reindex(columns=ordered_cols)
df = df.sort_values(by=["date","r_fighter"]).reset_index(drop=True)


df.to_csv("df.csv",index = False)



pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
