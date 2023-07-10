import curses
from curses.textpad import Textbox,rectangle
import random
from tabulate import tabulate
import pandas as pd
import time

#Imprimit texto de forma progresiva
def slow_print(pad,text,speed):
    for char in text:
        pad.addstr(char)
        pad.refresh()
        time.sleep(speed)

def die_gen(die,quant,mod):
    result = 0
    for tirada in range(quant):
        result += random.randint(1,die)
        result += mod
    return result

def box_end():
    return True
#Pandas-->ASCII
def draw_dataframe(stdscr, df):
    stdscr.clear()
    # Convert DataFrame to a formatted table
    table = tabulate(df, headers='keys', tablefmt='simple_grid')

    # Print the table in the curses window
    stdscr.addstr(1, 0, table)
    stdscr.refresh()

    # Wait for user input
#Creación de la tabla inicial de iniciativa
def tablenator(item):
    item = item.strip('\n')
    item = item.split(';') 
    return item
def read_pc_data():
    pc_data = open('resources\\pc_stats.csv','r+')
    pc_stats = pc_data.readlines()
    pc_data.close()
    pc_stats = list(map(tablenator,pc_stats))
    c_data_stats={'Character':[],'HP':[],'AC':[],'Str':[],'Dex':[],'Con':[],'Int':[],'Wis':[],'Chr':[]}
    pc_stats.pop(0)
    for item in pc_stats:
        for i in range(9):
            key = list(c_data_stats.keys())[i]
            c_data_stats[key].append(item[i])
    df_c_data = pd.DataFrame(c_data_stats)
    return df_c_data
pc_data = read_pc_data()
death_npc = pd.DataFrame({'Character':[]})
def call_inic_char(pad, pc_data,alto,ancho):
    df = pd.DataFrame(columns=['Character', 'Iniciativa', 'HP', 'Succes', 'Failure'])
    temp_win = curses.newwin(2, 40, (alto+4), (ancho+2))
    for pc in range(len(pc_data['Character'])):
        while True:
            temp_win.clear()
            slow_print(temp_win, f'Ingrese la iniciativa de {pc_data["Character"][pc]}\n', 0.01)
            rectangle(pad, 5, 3, 7, 16)
            min_win = curses.newwin(1, 3, (alto+8), (ancho+10))
            pad.refresh()
            box = Textbox(min_win)
            box.edit()
            try:
                inic = int(box.gather())
                min_win.clear()
                break
            except ValueError:
                slow_print(temp_win, '\nNo seas boludo, poné un número.', 0.01)
                temp_win.getch()
        new_row = pd.DataFrame({'Character': [pc_data["Character"][pc]], 'Iniciativa': [inic]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.iloc[pc, 2] = pc_data.iloc[pc, 1]
        df.iloc[pc,3] = 0
        df.iloc[pc,4]= 0
    temp_win.clear()
    min_win.clear()
    slow_print(temp_win, 'Valores Actualizados, inicializando', 0.02)
    slow_print(temp_win, '.....', 0.5)
    df = df.sort_values(by='Iniciativa',ascending=False).reset_index(drop=True)
    return df

def call_inic_enemy(pad,df,alto,ancho):
    pad.clear()
    slow_print(pad,f'{"-"*15}Añadir Enemigos{"-"*15}',0.01)
    temp_win = curses.newwin(2, 50, (alto+3), (ancho+1))
    rectangle(pad, 5, 3, 7, 16)
    min_win = curses.newwin(1, 3, (alto+8), (ancho+10))
    pad.refresh()
    box = Textbox(min_win)
    #Dex
    while True:
        temp_win.clear()
        slow_print(temp_win, 'Sección: Destreza\nIngrese el modificador de Destreza del NPC', 0.01)
        box.edit()
        try:
            dex = int(box.gather())
            min_win.clear()
            break
        except ValueError:
            slow_print(temp_win, '\nNo seas boludo, poné un número.', 0.01)
            temp_win.getch()
    #Die quant
    while True:
        temp_win.clear()
        slow_print(temp_win,'Sección: Vida\nIngrese la cantidad de dados para rollear la Vida',0.01)
        box.edit()
        try:   
            die_q = int(box.gather())
            min_win.clear()
            break
        except ValueError:
            slow_print(temp_win, '\nNo seas boludo, poné un número.', 0.01)
            temp_win.getch()
    #Die face
    while True:
        temp_win.clear()
        slow_print(temp_win,'Sección: Vida\nIngrese la cantidad de caras de estos dados',0.01)
        box.edit()
        try:
            die = int(box.gather())
            min_win.clear()
            break
        except ValueError:
            slow_print(temp_win, '\nNo seas boludo, poné un número.', 0.01)
            temp_win.getch()
    #Con
    while True:
        temp_win.clear()
        slow_print(temp_win,'Sección: Vida\nIngrese el modificador de Constitución del NPC',0.01)
        box.edit()
        try:
            con = int(box.gather())
            min_win.clear()
            break
        except ValueError:
            slow_print(temp_win, 'No seas boludo, poné un número.', 0.01)
            temp_win.getch()
    #Nombre
    while True:
        temp_win.clear()
        slow_print(temp_win,'Ingrese la cantidad de enemigos a crear',0.01)
        box.edit()
        try:
            enemys = int(box.gather())
            min_win.clear()
            break
        except ValueError:
            slow_print(temp_win,'No seas boludo, poné un número.',0.01)
            temp_win.getch()
    min_win = curses.newwin(1, 12, (alto + 8), (ancho+5))
    box = Textbox(min_win)
    for i in range(enemys):
        temp_win.clear()
        slow_print(temp_win,'Ingrese bajo que nombre será registrado el NPC',0.01)
        box.edit()
        enemy_name = box.gather()
        enemy_hp = die_gen(die,die_q,con)
        enemy_inic = random.randint(1,20) + dex
        new_row = pd.DataFrame({'Character': [enemy_name], 'Iniciativa': [enemy_inic], 'HP':[enemy_hp]})
        df = pd.concat([df, new_row], ignore_index=True)
    df = df.sort_values(by='Iniciativa',ascending=False).reset_index(drop=True)
    min_win.clear()
    temp_win.clear()
    min_win.refresh()
    temp_win.refresh()
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
                
stdscr=curses.initscr()
curses.noecho()
curses.cbreak()
alto,ancho = stdscr.getmaxyx()
marg_sup = int(alto*0.1)
marg_lat = int(ancho*0.1)

'''
curses.textpad.rectangle(win, uly, ulx, lry, lrx)
curses.newwin(nlines, ncols, begin_y, begin_x)
 '''
mit_alto = int((alto-marg_sup*2)*0.5)
mit_ancho = int((ancho-marg_lat*2)*0.5)
left_scr_up_out = curses.newwin(mit_alto,mit_ancho,(marg_sup),(marg_lat))
left_scr_dw_out = curses.newwin(mit_alto,mit_ancho,(marg_sup+mit_alto),marg_lat)
right_scr_out = curses.newwin((alto-marg_sup*2),mit_ancho,marg_sup,(mit_ancho + marg_lat+1))


left_scr_up = curses.newwin((mit_alto-3),(mit_ancho-2),(marg_sup+2),(marg_lat+1))
left_scr_dw = curses.newwin((mit_alto-3),(mit_ancho-2),(marg_sup+mit_alto+2),(marg_lat+1))
right_scr = curses.newwin((alto-marg_sup*2-3),(mit_ancho-2),(marg_sup+2),(mit_ancho + marg_lat + 2))
left_scr_dw_out.box()
left_scr_up_out.box()
right_scr_out.box()

right_scr_out.addstr(0,int(mit_ancho*0.5-9),'╖Orden de Combate╓')
right_scr_out.addstr(1,int(mit_ancho*0.5-9),'╚════════════════╝')
left_scr_up_out.addstr(0,int(mit_ancho*0.5-3),'╖Menu╓')
left_scr_up_out.addstr(1,int(mit_ancho*0.5-3),'╚════╝')
left_scr_dw_out.addstr(0,int(mit_ancho*0.5-9),'╖Enemigos Muertos╓')
left_scr_dw_out.addstr(1,int(mit_ancho*0.5-9),'╚════════════════╝')
left_scr_dw_out.refresh()
left_scr_up_out.refresh()
right_scr_out.refresh()




slow_print(left_scr_up,'\nPor favor, ingrese las Iniciativas de los jugadores citados:\n',0.01)
inic_pool = call_inic_char(left_scr_up,pc_data,marg_sup,marg_lat)

action = ''
while True:
    draw_dataframe(right_scr,inic_pool)
    left_scr_up.clear()
    slow_print(left_scr_up,f'{"-"*15}Menu{"-"*15}\nSeleccione una opción de la lista:\n(1)Agregar un NPC\n(2)Eliminar un NPC\n(3)Modificar la vida de un NPC\n(4)Iniciar Combate',0.01)
    rectangle(left_scr_up, 7, 3, 9, 16)
    min_win = curses.newwin(1, 3, (marg_sup+10), (marg_lat+10))
    left_scr_up.refresh()
    box = Textbox(min_win)
    box.edit()
    action = int(box.gather())
    if action == 1:
        inic_pool = call_inic_enemy(left_scr_up,inic_pool,marg_sup,marg_lat)
    elif action == 2:
        inic_pool = call_inic_del(left_scr_up,inic_pool,marg_sup,marg_lat)
    elif action == 3:
        inic_pool = hp_modifier(left_scr_up,inic_pool,marg_sup,marg_lat)
    elif action == 4:
        break
    else:
        slow_print(left_scr_up,'ERROR, seleccione una opción válida',0.01)

ronda = 0
while True:
    inic_pool_temp = inic_pool.copy()
    for pc in inic_pool_temp['Character']:
        while True:
            left_scr_up.clear()
            text_ronda = f'Ronda N°{ronda}'
            slow_print(left_scr_up,f'{"-"*15}Ronda N°{ronda}{"-"*15}',0.005)
            draw_dataframe(right_scr,inic_pool)
            temp_win = curses.newwin(6, 50, (marg_sup+3), (marg_lat+1))
            text_turno = f'Turno de {pc}'
            slow_print(temp_win,f'{"-"*int((len(text_ronda)+30-len(text_turno))/2)}{text_turno}{"-"*int((len(text_ronda)+30-len(text_turno))/2)}',0.01)
            if int(inic_pool.loc[inic_pool['Character']==pc,'HP'].iloc[0])<= 0:
                if pc in ['Ariel','Gallo','Iago','JF','Logan']:
                    if inic_pool_temp.loc[inic_pool_temp['Character']==pc,'Failure'].iloc[0] == 3:
                        slow_print(temp_win,f'\n{pc} Esta Muerto',0.02)
                        time.sleep(2)
                        break
                    inic_pool = death_saving(temp_win,left_scr_up,inic_pool,pc,marg_sup,marg_lat)
                if pc not in ['Ariel','Gallo','Iago','JF','Logan']:
                    if pc not in death_npc['Character'].values:
                        inic_pool, death_npc = del_char(inic_pool,pc,death_npc)
                        left_scr_dw.clear()
                        slow_print(left_scr_dw,f'{"-"*15}Lista de Enemigos Muertos{"-"*15}\n{death_npc["Character"].tolist()}',0.01)
                time.sleep(1)    
                break
            else:
                slow_print(temp_win,'\nSeleccione una acción:\n(1)Atacar/Curar\n(2)Agregar un NPC\n(3)Terminar turno',0.005)
                rectangle(left_scr_up, 7, 3, 9, 16)
                min_win = curses.newwin(1, 3, (marg_sup+10), (marg_lat+10))
                left_scr_up.refresh()
                box = Textbox(min_win)
                try:   
                    box.edit()
                    action = int(box.gather())
                except ValueError:
                    slow_print(temp_win,'\nERROR, Ingrese un número',0.01)
                    temp_win.getch()
                    continue
                if action == 1:
                    inic_pool = hp_modifier(left_scr_up,inic_pool,marg_sup,marg_lat)
                elif action == 2:
                    inic_pool = call_inic_enemy(left_scr_up,inic_pool,marg_sup,marg_lat)
                elif action == 3:
                    break
    ronda +=1
left_scr_up.getch()
right_scr.getch()
