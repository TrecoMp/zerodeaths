"""
FAZER CALCULO DOS SCORES
    melhor mapa
    pior mapa
    sinergia
    counter
    counterar
"""


import pandas as pd
from tkinter import *
from tkinter import ttk

map_select = "MAPA"
sinergy = []
receive_counter = []
apply_counter = []
df_champions = pd.read_excel("data/ZeroDeaths.xlsx", sheet_name='campeao')
df_maps = pd.read_excel("data/ZeroDeaths.xlsx", sheet_name='mapas')
list_maps = df_maps['MAPA'].to_list()
list_maps.sort()
list_champs = df_champions['name'].to_list()
list_champs.sort()
window = Tk()



class LargeComboboxCounter(Frame):
    def __init__(self, master, items, set_counter_func=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.selected_item = StringVar(master)
        self.combobox = ttk.Combobox(self, textvariable=self.selected_item, values=items, state="readonly", height=10)
        self.combobox.pack(fill="both", expand=True)

        if set_counter_func:
            self.combobox.bind("<<ComboboxSelected>>", lambda event: set_counter_func(self.selected_item.get()))

class LargeComboboxSinergy(Frame):
    def __init__(self, master, items, set_sinergy_func=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.selected_item = StringVar(master)
        self.combobox = ttk.Combobox(self, textvariable=self.selected_item, values=items, state='readonly', height=10)
        self.combobox.pack(fill="both", expand=True)

        if set_sinergy_func:
            self.combobox.bind("<<ComboboxSelected>>", lambda event: set_sinergy_func(self.selected_item.get()))


class LargeComboboxBan(Frame):
    def __init__(self, master, items, set_ban_func=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.selected_item = StringVar(master)
        self.combobox = ttk.Combobox(self, textvariable=self.selected_item, values=items, state='readonly', height=10)
        self.combobox.pack(fill="both", expand=True)

        if set_ban_func:
            self.combobox.bind("<<ComboboxSelected>>", lambda event: set_ban_func(self.selected_item.get()))

def set_ban(champ):
    global df_champions_score
    ban(champ)

    champs_table = LabelFrame(window, text="Score Champions")
    champs_table.place(height=800, width=600, relx=0.4, rely=0)
   
    tv = ttk.Treeview(champs_table)
    tv.place(relheight=1,relwidth=1)
    tvscrolly = Scrollbar(champs_table, orient="vertical", command=tv.yview)
    
    tv.configure(yscrollcommand=tvscrolly.set)
    tvscrolly.pack(side='right',fill="y")
    
    df_champions_score = df_champions_score.sort_values(by=['score','type','name'], ascending=[False, True, True])
    tv['column'] = list(df_champions_score.columns)
    tv['show'] = "headings"

    
    for column in tv['column']:
        tv.heading(column,text=column)
    
    
    df_rows = df_champions_score.to_numpy().tolist()
    for row in df_rows:
        tv.insert("","end",values=row)

def ban(champ):
    global list_champs
    global df_champions_score

    df_champions_score = df_champions_score[df_champions_score['name'] != champ]
    list_champs.remove(champ)

    

def set_champ_map(mapa):    
    df_best_maps = df_champions[df_champions['best_maps'].str.contains(mapa, na=False)]
    df_worst_maps = df_champions[df_champions['worst_maps'].str.contains(mapa, na=False)]
    global df_champions_score
    df_champions_score = df_champions[['name','type']]

    df_champions_score['score'] = 0

    for index,row in df_champions_score.iterrows():
        if row['name'] in df_best_maps['name'].values:
            df_champions_score.loc[index,'score'] = df_champions_score.loc[index,'score'] + 1
        
        if row['name'] in df_worst_maps.values:
            df_champions_score.loc[index,'score'] = df_champions_score.loc[index,'score'] - 1

    champs_table = LabelFrame(window, text="Score Champions")
    champs_table.place(height=800, width=600, relx=0.4, rely=0)
   
    tv = ttk.Treeview(champs_table)
    tv.place(relheight=1,relwidth=1)
    tvscrolly = Scrollbar(champs_table, orient="vertical", command=tv.yview)
    
    tv.configure(yscrollcommand=tvscrolly.set)
    tvscrolly.pack(side='right',fill="y")
    
    df_champions_score = df_champions_score.sort_values(by=['score','type','name'], ascending=[False, True, True])
    tv['column'] = list(df_champions_score.columns)
    tv['show'] = "headings"

    
    for column in tv['column']:
        tv.heading(column,text=column)
    
    
    df_rows = df_champions_score.to_numpy().tolist()
    for row in df_rows:
        tv.insert("","end",values=row)

    return None

def set_sinergy(champ):
    global df_champions_score
    champ_sinergys = df_champions.loc[df_champions['name'] == champ,'sinergy'].values[0].split(';')
    for n in champ_sinergys:
        df_champions_score.loc[df_champions_score['name'] == n, 'score'] += 1
    

    champs_table = LabelFrame(window, text="Score Champions")
    champs_table.place(height=800, width=600, relx=0.4, rely=0)
   
    ban(champ)
    tv = ttk.Treeview(champs_table)
    tv.place(relheight=1,relwidth=1)
    tvscrolly = Scrollbar(champs_table, orient="vertical", command=tv.yview)
    
    tv.configure(yscrollcommand=tvscrolly.set)
    tvscrolly.pack(side='right',fill="y")
    
    df_champions_score = df_champions_score.sort_values(by=['score','type','name'], ascending=[False, True, True])
    tv['column'] = list(df_champions_score.columns)
    tv['show'] = "headings"

    for column in tv['column']:
        tv.heading(column,text=column)
    
    
    df_rows = df_champions_score.to_numpy().tolist()
    for row in df_rows:
        tv.insert("","end",values=row)

    
    return None

def set_counter(champ):
    global df_champions_score
    champ_counter = df_champions.loc[df_champions['name'] == champ,'counters'].values[0].split(';')
    for n in champ_counter:
         df_champions_score.loc[df_champions_score['name'] == n, 'score'] += 1

    champs_get_counter = df_champions.loc[df_champions['counters'].str.contains(champ, case=False),'name']
    df_champions_score.loc[df_champions_score['name'].isin(champs_get_counter), 'score'] -= 1

    champs_table = LabelFrame(window, text="Score Champions")
    champs_table.place(height=800, width=600, relx=0.4, rely=0)
   
    ban(champ)

    tv = ttk.Treeview(champs_table)
    tv.place(relheight=1,relwidth=1)
    tvscrolly = Scrollbar(champs_table, orient="vertical", command=tv.yview)
    
    tv.configure(yscrollcommand=tvscrolly.set)
    tvscrolly.pack(side='right',fill="y")
    
    df_champions_score = df_champions_score.sort_values(by=['score','type','name'], ascending=[False, True, True])
    tv['column'] = list(df_champions_score.columns)
    tv['show'] = "headings"

    for column in tv['column']:
        tv.heading(column,text=column)
    
    
    df_rows = df_champions_score.to_numpy().tolist()
    for row in df_rows:
        tv.insert("","end",values=row)
    
    return None



def main():
    window.title("ZeroDeaths")
    window.geometry("1000x800")

    text_labelmap = Label(window, text="Escolha o mapa a ser jogado")
    text_labelmap.place(relx=0, rely=0)

    get_map = StringVar(window)
    get_map.set(map_select)
    set_champ_map("map_select")
    menu_map = OptionMenu(window,get_map,*list_maps, command=lambda mapa: set_champ_map(mapa))
    menu_map.place(relx=0, rely=0.03)
    #############################################################

    text_ban_myteam1 = Label(window, text="FisrtBan")
    text_ban_myteam1.place(relx=0, rely=0.07)
    select_ban_myteam1 = LargeComboboxBan(window, list_champs, set_ban_func=set_ban)
    select_ban_myteam1.place(relx=0, rely=0.09)

    #############################################################

    text_ban_myteam2 = Label(window, text="SecondBan")
    text_ban_myteam2.place(relx=0, rely=0.11)
    select_ban_myteam2 = LargeComboboxBan(window, list_champs, set_ban_func=set_ban)
    select_ban_myteam2.place(relx=0, rely=0.13)
    
    #############################################################

    text_champ_myteam1 = Label(window, text="champ01")
    text_champ_myteam1.place(relx=0, rely=0.15)
    select_champ_myteam1 = LargeComboboxSinergy(window, list_champs, set_sinergy_func=set_sinergy)
    select_champ_myteam1.place(relx=0, rely = 0.17)

    #############################################################

    text_champ_myteam2 = Label(window, text="champ02")
    text_champ_myteam2.place(relx=0, rely=0.19)
    select_champ_myteam2 = LargeComboboxSinergy(window, list_champs, set_sinergy_func=set_sinergy)
    select_champ_myteam2.place(relx=0, rely = 0.21)

    #############################################################

    text_champ_myteam3 = Label(window, text="champ03")
    text_champ_myteam3.place(relx=0, rely=0.23)
    select_champ_myteam3 = LargeComboboxSinergy(window, list_champs, set_sinergy_func=set_sinergy)
    select_champ_myteam3.place(relx=0, rely = 0.25)

    #############################################################

    text_ban_myteam3 = Label(window, text="ThirdBan")
    text_ban_myteam3.place(relx=0, rely=0.27)
    select_ban_myteam3 = LargeComboboxBan(window, list_champs, set_ban_func=set_ban)
    select_ban_myteam3.place(relx=0, rely=0.29)


    #############################################################

    text_champ_myteam4 = Label(window, text="champ04")
    text_champ_myteam4.place(relx=0, rely=0.31)
    select_champ_myteam4 = LargeComboboxSinergy(window, list_champs, set_sinergy_func=set_sinergy)
    select_champ_myteam4.place(relx=0, rely = 0.33)

    #############################################################

    text_champ_myteam5 = Label(window, text="champ05")
    text_champ_myteam5.place(relx=0, rely=0.35)
    select_champ_myteam5 = LargeComboboxSinergy(window, list_champs, set_sinergy_func=set_sinergy)
    select_champ_myteam5.place(relx=0, rely = 0.37)

    #############################################################
    
    text_ban_enemyteam1 = Label(window, text="FisrtBan")
    text_ban_enemyteam1.place(relx=0.2, rely=0.07)
    select_ban_enemyteam1 = LargeComboboxBan(window, list_champs, set_ban_func=set_ban)
    select_ban_enemyteam1.place(relx=0.2, rely=0.09)
    
    #############################################################

    text_ban_enemyteam2 = Label(window, text="SecondBan")
    text_ban_enemyteam2.place(relx=0.2, rely=0.11)
    select_ban_enemyteam2 = LargeComboboxBan(window, list_champs, set_ban_func=set_ban)
    select_ban_enemyteam2.place(relx=0.2, rely=0.13)

    #############################################################

    text_champ_enemyteam1 = Label(window, text="enemy01")
    text_champ_enemyteam1.place(relx=0.2, rely=0.15)
    select_champ_enemyteam1 = LargeComboboxCounter(window,list_champs,set_counter_func=set_counter)
    select_champ_enemyteam1.place(relx=0.2, rely = 0.17)
    
    #############################################################

    text_champ_enemyteam2 = Label(window, text="enemy02")
    text_champ_enemyteam2.place(relx=0.2, rely=0.19)
    select_champ_enemyteam2 = LargeComboboxCounter(window,list_champs,set_counter_func=set_counter)
    select_champ_enemyteam2.place(relx=0.2, rely = 0.21)

    #############################################################

    text_champ_enemyteam3 = Label(window, text="enemy03")
    text_champ_enemyteam3.place(relx=0.2, rely=0.23)
    select_champ_enemyteam3 = LargeComboboxCounter(window,list_champs,set_counter_func=set_counter)
    select_champ_enemyteam3.place(relx=0.2, rely = 0.25)

    #############################################################

    text_ban_enemyteam3 = Label(window, text="ThirdBan")
    text_ban_enemyteam3.place(relx=0.2, rely=0.27)
    select_ban_enemyteam3 = LargeComboboxBan(window, list_champs, set_ban_func=set_ban)
    select_ban_enemyteam3.place(relx=0.2, rely=0.29)

    #############################################################

    text_champ_enemyteam4 = Label(window, text="enemy04")
    text_champ_enemyteam4.place(relx=0.2, rely=0.31)
    select_champ_enemyteam4 = LargeComboboxCounter(window,list_champs,set_counter_func=set_counter)
    select_champ_enemyteam4.place(relx=0.2, rely = 0.33)

    #############################################################

    text_champ_enemyteam5 = Label(window, text="enemy05")
    text_champ_enemyteam5.place(relx=0.2, rely=0.35)
    select_champ_enemyteam5 = LargeComboboxCounter(window,list_champs,set_counter_func=set_counter)
    select_champ_enemyteam5.place(relx=0.2, rely = 0.37)
    
    
    
    
    window.mainloop()

if __name__ == "__main__":
    main()