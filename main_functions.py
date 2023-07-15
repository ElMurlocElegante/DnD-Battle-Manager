
from suport_functions import *
import curses
from curses.textpad import rectangle,Textbox
import curses.textpad

class Character:
    def __init__(self,name):
        self.name = name
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

def call_inic_char(pad,pad_b,pad_n,pc_data,col1,col2):
    df = pd.DataFrame(columns=['Character', 'Iniciativa', 'HP', 'Succes', 'Failure'])
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
                        if new_row['Character'][0] not in df['Character'].tolist():
                            df = pd.concat([df, new_row], ignore_index=True)
                            df.iloc[pc, 2] = pc_data.iloc[pc, 1]
                            df.iloc[pc,3] = 0
                            df.iloc[pc,4]= 0
                    break
                except:
                    for i in range(6):
                        pad.addstr(y,int((x-24)/2),'ERROR, Ingrese un Número')
                        pad.refresh()
                        time.sleep(0.1)
                        pad.addstr(y,int((x-24)/2),'ERROR, Ingrese un Número',col2)
                        pad.refresh()
                        time.sleep(0.1)
                    pad.addstr(y,int((x-24)/2),' '*24)
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
    return df

def call_inic_enemy(pad,pad_b,pad_n,pad_t,df,col1,col2):
    pad.clear()
    y,x=pad.getmaxyx()
    if x % 2 != 0:
        x -=1
    box_inator(pad_b,'Añadir Enemigo','num')
    pad_b.refresh()
    text_list = ['Dex Mod','Dice Quant','Dice Faces','Con Mod','Cantidad de Enemigos',]
    key = ' '
    selec = 0
    dex,dice_quant,dice_face,con,enemys = None,None,None,None,None
    while True:

        if key == 'KEY_UP':
            selec -= 1
        elif key == 'KEY_DOWN':
            selec += 1
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
                enemys = get_input_data(pad,pad_n,x,selec,col1,col2)
                selec += 1
            elif selec == 5:
                if dex != None and dice_quant != None and dice_face != None and con != None and enemys != None:
                    break
                else:
                    for i in range(6):
                        pad.addstr(y,int((x-30)/2),'ERROR, ingrese todos los datos')
                        pad.refresh()
                        time.sleep(0.1)
                        pad.addstr(y,int((x-30)/2),'ERROR, ingrese todos los datos',col2)
                        pad.refresh()
                        time.sleep(0.1)
                    pad.addstr(y,int((x-30)/2),' '*30)
                    pad.refresh()
                    time.sleep(0.5)
                    
        if selec < 0:
            selec = 5
        elif selec >5:
            selec = 0
        for i in range(len(text_list)):
            pad.addstr(i,int(x*0.1-1),' '+text_list[i]+' ')
        pad.addstr(len(text_list),int(x/2-2),' OK ')
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
    enemy_names = []
    while True:
        if key == 'KEY_UP':
            selec -= 1
        elif key == 'KEY_DOWN':
            selec += 1
        elif key == '\n':
            nombre = get_input_data_txt(pad,pad_t,x,selec,col1,col2)
            enemy_names.append(nombre)
        for i in range(enemys):
            pad.addstr(i,int(x*0.1),f'Enemigo N°{i+1}')
    for i in range(enemys):
        nombre = get_input_data_txt(pad,pad_t,x,i,col1,col2)
        enemy_hp = die_gen(dice_face,dice_quant,con)
        enemy_inic = random.randint(1,20) + dex
        new_row = pd.DataFrame({'Character': [nombre], 'Iniciativa': [enemy_inic], 'HP':[enemy_hp]})
        df = pd.concat([df, new_row], ignore_index=True)
    df = df.sort_values(by='Iniciativa',ascending=False).reset_index(drop=True)
    pad.clear()

    return df

def call_inic_del(pad,df,alto,ancho):
    pad.clear()
    slow_print(pad,f'{"-"*15}Remover Enemigos{"-"*15}',0.01)
    temp_win = curses.newwin(2, 50, (alto + 4), (ancho+3))
    while True:
        try:
            temp_win.clear()
            rectangle(pad, 5, 3, 7, 16)
            pad.refresh()
            slow_print(temp_win,'Ingrese el Índice del personaje que desea eliminar',0.01)
            min_win = curses.newwin(1, 3, (alto+8), (ancho+10))
            box = Textbox(min_win)
            box.edit()
            del_char = int(box.gather())
            if del_char < 0 or del_char > (len(df['Character'])-1):
                slow_print(temp_win,'ERROR, Ingrese un número',0.01)
                continue   
            break
        except ValueError:
            slow_print(temp_win,'ERROR, Ingrese un número',0.01)
            temp_win.getch()
    df = df.drop([del_char])
    df = df.sort_values('Iniciativa',ascending = False).reset_index(drop=True)
    temp_win.clear()
    min_win.clear()
    return df

def del_char(df,pc,df_d):
    pc_index = df['Character'].tolist().index(pc)
    df = df.drop([pc_index])
    df = df.sort_values('Iniciativa',ascending = False).reset_index(drop=True)
    new_row = pd.DataFrame({'Character': [pc]})
    df_d = pd.concat([df_d,new_row],ignore_index=True)
    return df,df_d
def hp_modifier(pad,df,alto,ancho):
    pad.clear()
    slow_print(pad,f'{"-"*15}Modificar Vida{"-"*15}',0.01)
    temp_win = curses.newwin(3, 50, (alto+3), (ancho+3))
    rectangle(pad, 5, 3, 7, 16)
    temp_win.clear()
    slow_print(temp_win,'Ingrese el índice del personaje a alterar:',0.01)
    min_win = curses.newwin(1, 4, (alto+8), (ancho+10))
    pad.refresh()
    box = Textbox(min_win)
    while True:
        box.edit()
        try:
            selec = int(box.gather())
            if selec < 0 or selec>(len(df['Character'])):
                slow_print(temp_win,'ERROR, Ingrese un valor válido',0.01)
                temp_win.clear()
                continue
            break
        except ValueError:
            slow_print(temp_win,'\nERROR, Ingrese un número',0.01)
            temp_win.getch()

    while True:
        min_win.clear( )
        temp_win.clear()
        slow_print(temp_win,'Ingrese la vida a substraer o agregar\n(con un menos adelante)',0.01)
        box.edit()
        try:

            hp_mod = int(box.gather())
            break
        except ValueError:
            slow_print(temp_win,'\nERROR, Ingrese un número',0.01)
            temp_win.getch()
    temp_win.clear()
    min_win.clear()
    df.iloc[selec,2]=(int(df.iloc[selec,2]) - hp_mod)
    df = df.sort_values('Iniciativa',ascending = False)
    df = df.reset_index(drop=True)    
    slow_print(temp_win,'Valores Actualizados.',0.02)
    return df

def death_saving(pad,pad2,df,pc,alto,ancho):
    slow_print(pad,f'\n{pc} Está abatido.\nHaga un tiro de salvación:',0.01)
    while True:

        rectangle(pad2, 7, 3, 9, 16)
        min_win = curses.newwin(1, 3, (alto+10), (ancho+10))
        pad2.refresh()
        box = Textbox(min_win)
        try:
            box.edit()
            result = int(box.gather())
            if result < 1 or result > 20:
                continue
            break
        except:
            slow_print(pad,'ERROR, Ingrese un número',0.01)
            pad.getch()
    if result == 1:
        df.loc[df['Character'] == pc,'Failure'] += 2
    elif result in range(2,10):
        df.loc[df['Character'] == pc,'Failure'] += 1
    elif result in range(10,20):
        df.loc[df['Character'] == pc,'Succes'] += 1
    elif result == 20:
        df.loc[df['Character'] == pc,'Succes'] = 3
    
    if df.loc[df['Character'] == pc,'Failure'].iloc[0] >= 3:
        df.loc[df['Character'] == pc,'Failure'] = 3
    if df.loc[df['Character'] == pc,'Succes'].iloc[0] == 3:
        df.loc[df['Character'] == pc,'Failure'] = 0
        df.loc[df['Character'] == pc,'Succes'] = 0
        df.loc[df['Character'] == pc,'HP'] = 1
        slow_print(pad, f'\n{pc} Logró todos los tiros de salvación',0.02)
    return df