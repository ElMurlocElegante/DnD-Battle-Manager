
from suport_functions import *
from menus import *
import curses
import curses.textpad

class Character:
    def __init__(self,name):
        self.name = name
    def set_name(self,value):
        self.name = value
    def get_name(self):
        return self.name
    def set_inic(self,value):
        self.inic = value
    def get_inic(self):
        return self.inic
    def set_hp(self,value):
        self.hp = value
    def get_hp(self):
        return self.hp
    def set_ac(self,value):
        self.ac = value
    def get_ac(self):
        return self.ac

def call_inic_char(pad,pad_b,pad_n,df_dmg,col1,col2):
    file = open("resources\\battle_log.txt",mode='w')
    file.write('')
    file.close()
    pc_data = pd.read_csv('resources\\pc_stats.csv',sep=';')
    df = pd.DataFrame(columns=['Character', 'Iniciativa', 'Max HP','HP','AC', 'S', 'F'])
    txt = 'Ingrese la iniciativa de:'
    y,x = pad.getmaxyx()

    if (x-len(txt))%2 != 0:
        x -=1
    box_inator(pad_b,"Iniciativa",'num')
    pc_list = []
    for pc in pc_data['Character']:
        pc = Character(pc)
        pc_list.append(pc)
    
        
    for i in range(0,len(pc_data['Character'])):
        pad.addstr(i,int(x*0.1),str(pc_list[i].get_name()))
    selec = 0
    key=''
    while True:
        
        
        if key == 'KEY_UP':
            selec -= 1
        elif key == 'KEY_DOWN':
            selec += 1
        elif key == '\n':
            if selec == 5:
                try:
                    for pc in range(len(pc_data['Character'])):
                        new_row = pd.DataFrame({'Character': [pc_data["Character"][pc]], 'Iniciativa': [int(pc_list[pc].get_inic())]})
                        new_row2 = pd.DataFrame({'Character':[pc_data["Character"][pc]],'Damage':[0]})
                        if new_row['Character'][0] not in df['Character'].tolist() and new_row2['Character'][0] not in df_dmg['Character'].tolist():
                            df = pd.concat([df, new_row], ignore_index=True)
                            df_dmg = pd.concat([df_dmg, new_row2], ignore_index=True)
                            df.iloc[pc, 2] = pc_data.iloc[pc, 1]
                            df.iloc[pc, 3] = pc_data.iloc[pc, 2]
                            df.iloc[pc, 4] = pc_data.iloc[pc, 3]
                            df.iloc[pc,5] = 0
                            df.iloc[pc,6]= 0
                    break
                except:
                    for i in range(6):
                        pad.addstr(y-1,int((x-30)/2),'ERROR, Ingrese todos los Datos')
                        pad.refresh()
                        time.sleep(0.1)
                        pad.addstr(y-1,int((x-30)/2),'ERROR, Ingrese todos los Datos',col2)
                        pad.refresh()
                        time.sleep(0.1)
                    pad.addstr(y-1,int((x-30)/2),' '*30)
                    pad.refresh()
                    time.sleep(0.5)
            else:
                pc_list[selec].set_inic(get_input_data(pad,pad_n,x,selec,col1,col2))
                selec +=1


        if selec < 0:
            selec = 5
        elif selec >5:
            selec = 0
        for i in range(0,len(pc_data['Character'])):
            pad.addstr(i,int(x*0.1-1),' '+str(pc_list[i].get_name())+' ')
        pad.addstr(int(len(pc_data['Character'])),int(x/2-2),' OK ')
        try:
            pad.addstr(selec,int(x*0.1-1),'»'+' '*len(str(pc_list[selec].get_name()))+'«')
            pad.addstr(selec,int(x*0.1),str(pc_list[selec].get_name()),curses.A_STANDOUT)
        except:
            pad.addstr(selec,int(x/2-2),'»'+' '*2+'«')
            pad.addstr(int(len(pc_data['Character'])),int(x/2-1),'OK',curses.A_STANDOUT)
        pad_b.refresh()
        pad.refresh()
        key = pad.getkey()

    pad.addstr(y-1,int(x/2-11),'['+'░'*20+']')
    for i in range(20):
        pad.addstr(y-1,int(x/2-10+i),'▓')
        pad.refresh()
        time.sleep(0.15)
    time.sleep(1)
    df = df.sort_values(by='Iniciativa',ascending=False).reset_index(drop=True)
    return df, df_dmg

def call_inic_enemy(pad,pad_b,pad_n,pad_t,df,df_dmg,col1,col2):
    pad.clear()
    y,x=pad.getmaxyx()
    if x % 2 != 0:
        x -=1
    box_inator(pad_b,'Añadir Enemigo','num')
    pad_b.refresh()
    text_list = ['Dex Mod','Dice Quant','Dice Faces','Con Mod','AC','Cantidad de Enemigos',]
    key = ' '
    selec = 0
    dex,dice_quant,dice_face,con,ac,enemies = None,None,None,None,None,None
    while True:

        if key == 'KEY_UP':
            selec -= 1
        elif key == 'KEY_DOWN':
            selec += 1
        elif key == 'q' or key == 'Q':
            return df,df_dmg
        elif key == '\n':
            if selec == 0:
                dex = get_input_data(pad,pad_n,x,selec,col1,col2)
                selec += 1
            elif selec == 1:
                dice_quant = get_input_data(pad,pad_n,x,selec,col1,col2)
                selec += 1
            elif selec == 2:
                dice_face = get_input_data(pad,pad_n,x,selec,col1,col2)
                selec += 1
            elif selec == 3:
                con = get_input_data(pad,pad_n,x,selec,col1,col2)
                selec += 1
            elif selec == 4:
                ac = get_input_data(pad,pad_n,x,selec,col1,col2)
                selec += 1
            elif selec == 5:
                enemies = get_input_data(pad,pad_n,x,selec,col1,col2)
                selec += 1
            elif selec == 6:
                if dex != None and dice_quant != None and dice_face != None and con != None and enemies != None and ac != None:
                    break
                else:
                    for i in range(6):
                        pad.addstr(y-1,int((x-30)/2),'ERROR, ingrese todos los datos')
                        pad.refresh()
                        time.sleep(0.1)
                        pad.addstr(y-1,int((x-30)/2),'ERROR, ingrese todos los datos',col2)
                        pad.refresh()
                        time.sleep(0.1)
                    pad.addstr(y,int((x-30)/2),' '*30)
                    pad.refresh()
                    time.sleep(0.5)
                    
        if selec < 0:
            selec = 6
        elif selec >6:
            selec = 0
        for i in range(len(text_list)):
            pad.addstr(i,int(x*0.1-1),' '+text_list[i]+' ')
        pad.addstr(len(text_list),int(x/2)-2,' OK ')
        pad.addstr(y-1,int(x-len('Q para volver al Menú')-2),'Q para volver al Menú')
        try:
            pad.addstr(selec,int(x*0.1-1),'»'+' '*len(text_list[selec])+'«')
            pad.addstr(selec,int(x*0.1),text_list[selec],curses.A_STANDOUT)
        except:
            pad.addstr(selec,int(x/2-2),'»'+' '*2+'«')
            pad.addstr(selec,int(x/2-1),'OK',curses.A_STANDOUT)
        pad.refresh()
        key = pad.getkey()
    box_inator(pad_b,'Nombre de Enemigo','txt')
    pad_b.refresh()
    key = ' '
    selec = 0
    enemy_list = []
    enemy_names = []
    
    for i in range(enemies):
        enemy_list.append(f'Enemigo N°{i+1}')
    for npc in enemy_list:
        npc = Character(npc)
        enemy_names.append(npc)
    max_selec = len(enemy_list)
    while True:
        
        if key == 'KEY_UP':
            selec -= 1
        elif key == 'KEY_DOWN':
            selec += 1
        elif key == 'q' or key == 'Q':
            return df,df_dmg
        elif key == '\n':
            try:
                enemy_names[selec].set_name(get_input_data_txt(pad,pad_t,x,selec,col1,col2))
                selec +=1
            except:
                break
        if selec <0:
            selec = max_selec
        elif selec >max_selec:
            selec = 0
        for i in range(max_selec):
            pad.addstr(i,int(x*0.1-1),' '+str(enemy_list[i])+' ')
        pad.addstr(max_selec,int(x/2-2),' OK ')
        pad.addstr(y-1,int(x-len('Q para volver al Menú')-2),'Q para volver al Menú')
        try:
            pad.addstr(selec,int(x*0.1)-1,'»'+str(enemy_list[selec])+'«')
            pad.addstr(selec,int(x*0.1),str(enemy_list[selec]),curses.A_STANDOUT)
        except:
            pad.addstr(selec,int(x/2-2),'»'+' '*2+'«')
            pad.addstr(selec,int(x/2-1),'OK',curses.A_STANDOUT)

        pad.refresh()
        key = pad.getkey()
    for i in range(enemies):
        enemy_names[i].set_hp(die_gen(dice_face,dice_quant,con))
        enemy_names[i].set_inic(random.randint(1,20) + dex) 
        new_row = pd.DataFrame({'Character': [str(enemy_names[i].get_name())], 'Iniciativa': [int(enemy_names[i].get_inic())], 'Max HP':[int(enemy_names[i].get_hp())],'HP':[int(enemy_names[i].get_hp())],'AC':[int(ac)]})
        new_row2 = pd.DataFrame({'Character':[str(enemy_names[i].get_name())],'Damage':[0]})
        df = pd.concat([df, new_row], ignore_index=True)
        df_dmg = pd.concat([df_dmg, new_row2],ignore_index=True)
    df = df.sort_values(by='Iniciativa',ascending=False).reset_index(drop=True)
    pad.clear()

    return df,df_dmg

def call_inic_del(pad,pad_b,df):
    selec = multi_page_menu(pad,pad_b,df,'Eliminar Enemigo')
    if selec == 'q':
        return df
    else:
        df = df.drop([selec])
        df = df.sort_values('Iniciativa',ascending = False).reset_index(drop=True)
        pad.clear()
        pad.refresh()
        return df

def del_char(df,pc,df_d):
    pc_index = df['Character'].tolist().index(pc)
    df = df.drop([pc_index])
    df = df.sort_values('Iniciativa',ascending = False).reset_index(drop=True)
    df_d.append(pc)
    return df,df_d
def inic_modifier(pad,pad_b,pad_n,df,col1,col2):
    y,x = pad.getmaxyx()
    y = int(y/2)
    selec = multi_page_menu(pad,pad_b,df,'Modificar Iniciativa') 
    if selec == 'q':
        return df
    else:
        pad.clear()
        txt = f'Modificar Iniciativa de {df.iloc[selec,0]}'
        txt2 = f'Iniciativa actual: {df.iloc[selec,1]}'
        pad.addstr(0,int((x-len(txt))/2),txt)
        pad.addstr(1,int((x-len(txt2))/2),txt2)
        box_inator(pad_b,'Ingrese un Valor','num')
        pad_b.refresh()
        pad.refresh()
        inic_mod = get_input_data(pad,pad_n,x,y,col1,col2)
        df.iloc[selec,1]= inic_mod
        df = df.sort_values('Iniciativa',ascending = False)
        df = df.reset_index(drop=True)
        pad.addstr(1,int((x-len(txt2))/2),txt2)
        time.sleep(0.5)
        pad.refresh()
        pad.clear()
        
        return df
def hp_modifier(pad,pad_b,pad_n,df,df_dmg,pc,col1,col2):
    y,x = pad.getmaxyx()
    y = int(y/2)
    selec = multi_page_menu(pad,pad_b,df,'Modificar HP')
    if selec == 'q':
        return df,df_dmg
    else:
        pad.clear()
        txt = f'Modificar HP de {df.iloc[selec,0]}'
        txt2 = f'Vida actual: {df.iloc[selec,3]}/{df.iloc[selec,2]}'
        pad.addstr(0,int((x-len(txt))/2),txt)
        pad.addstr(1,int((x-len(txt2))/2),txt2)
        box_inator(pad_b,'Ingrese un Valor','num')
        pad_b.refresh()
        pad.refresh()
        hp_mod = get_input_data(pad,pad_n,x,y,col1,col2)
        df.iloc[selec,3]=(int(df.iloc[selec,3]) - hp_mod)
        df = df.sort_values('Iniciativa',ascending = False)
        df = df.reset_index(drop=True)
        pad.addstr(1,int((x-len(txt2))/2),txt2)
        time.sleep(0.5)
        pad.refresh()
        pad.clear()
        if hp_mod > 0:
            df_dmg.loc[df_dmg['Character'] == pc,'Damage'] += hp_mod
            df_dmg = df_dmg.sort_values(by='Damage',ascending=False).reset_index(drop=True)

        file = open('resources\\battle_log.txt',mode='a')
        if hp_mod>0:
            file.write(f'[{time.asctime()}]{pc} Infligió {hp_mod} de daño a {df["Character"][selec]}\n')
        elif hp_mod<0:
            file.write(f'[{time.asctime()}]{pc} Curó {-hp_mod} de vida a {df["Character"][selec]}\n')
        else:
            file.write(f'[{time.asctime()}]{pc} Falló su ataque a {df["Character"][selec]}\n')
        file.close()
        return df, df_dmg

def reaction_mod(pad,pad_b,pad_n,df,df_dmg,col1,col2):
    y,x = pad.getmaxyx()
    y = int(y/2)
    pc = multi_page_menu(pad,pad_b,df,'Reacción PC')
    if pc == 'q':
        return df,df_dmg
    selec = multi_page_menu(pad,pad_b,df,'Modificar HP')
    if selec == 'q':
        return df,df_dmg
    else:
        pad.clear()
        txt = f'Modificar HP de {df.iloc[selec,0]}'
        txt2 = f'Vida actual: {df.iloc[selec,3]}/{df.iloc[selec,2]}'
        pad.addstr(0,int((x-len(txt))/2),txt)
        pad.addstr(1,int((x-len(txt2))/2),txt2)
        box_inator(pad_b,'Ingrese un Valor','num')
        pad_b.refresh()
        pad.refresh()
        hp_mod = get_input_data(pad,pad_n,x,y,col1,col2)
        df.iloc[selec,3]=(int(df.iloc[selec,3]) - hp_mod)
        df = df.sort_values('Iniciativa',ascending = False)
        df = df.reset_index(drop=True)
        pad.addstr(1,int((x-len(txt2))/2),txt2)
        time.sleep(0.5)
        pad.refresh()
        pad.clear()
        if hp_mod > 0:
            df_dmg.loc[df_dmg['Character'] == pc,'Damage'] += hp_mod
            df_dmg = df_dmg.sort_values(by='Damage',ascending=False).reset_index(drop=True)

        file = open('resources\\battle_log.txt',mode='a')
        if hp_mod>0:
            file.write(f'[{time.asctime()}]{df["Character"][pc]} Infligió {hp_mod} de daño a {df["Character"][selec]}\n')
        elif hp_mod<0:
            file.write(f'[{time.asctime()}]{df["Character"][pc]} Curó {-hp_mod} de vida a {df["Character"][selec]}\n')
        else:
            file.write(f'[{time.asctime()}]{df["Character"][pc]} Falló su ataque a {df["Character"][selec]}\n')
        file.close()
        return df, df_dmg
def death_saving(pad,pad_b,pad_n,df,pc,col1,col2):
    box_inator(pad_b,'Tiros de Salvación','num')
    y,x = pad.getmaxyx()
    txt = f'Tiene {df.loc[df["Character"] == pc,"F"].iloc[0]} Tiros Fallados y {df.loc[df["Character"] == pc,"S"].iloc[0]} Tiros Logrados'
    txt2 = f'{pc} Logró todos los tiros de salvación'
    txt3 = 'Y se encuentra estabilizado'
    pad_b.refresh()
    pad.addstr(0,int((x-len(f'{pc} Está abatido'))/2),f'{pc} Está abatido')
    pad.refresh()
    if df.loc[df['Character'] == pc,'S'].iloc[0] != 3:
        pad.addstr(1,int((x-len(txt))/2),txt)
        pad.refresh()
        result = get_input_data(pad,pad_n,int(x/2),int(y/2),col1,col2)
        if result == 1:
            df.loc[df['Character'] == pc,'F'] += 2
        elif result in range(2,10):
            df.loc[df['Character'] == pc,'F'] += 1
        elif result in range(10,20):
            df.loc[df['Character'] == pc,'S'] += 1
        elif result == 20:
            df.loc[df['Character'] == pc,'F'] = 0
            df.loc[df['Character'] == pc,'S'] = 0
            df.loc[df['Character'] == pc,'HP'] = 1
        
        if df.loc[df['Character'] == pc,'F'].iloc[0] >= 3:
            df.loc[df['Character'] == pc,'F'] = 3
        if df.loc[df['Character'] == pc,'S'].iloc[0] == 3:
            df.loc[df['Character'] == pc,'F'] = 0
            
            pad.addstr(3,int((x-len(txt2))/2),txt2)
            pad.addstr(4,int((x-len(txt3))/2),txt3)
    else: 
        pad.addstr(3,int((x-len(txt2))/2),txt2)
        pad.addstr(4,int((x-len(txt3))/2),txt3)
    pad.addstr(1,int((x-len(txt))/2),txt)
    pad.refresh()
    time.sleep(0.5)
    return df
