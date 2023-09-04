import random
from tabulate import tabulate
import pandas as pd
import curses.textpad


#Imprimit texto de forma progresiva
def die_gen(die,quant,mod):
    result = 0
    for tirada in range(quant):
        result += random.randint(1,die)
        result += mod
    return result


#Pandas-->ASCII
def draw_dataframe(pad, df):
    pad.clear()
    y,x=pad.getmaxyx()
    # Convert DataFrame to a formatted table
    table = tabulate(df, headers='keys', tablefmt='simple_grid',showindex=False)
    # Print the table in the curses window
    pad.addnstr(0,0, table,y*(len(table.split('\n')[0])))
    pad.refresh()

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

def box_inator(pad,text,type):
    pad.clear()
    y,x = pad.getmaxyx()
    #Crear caja  de texto
    if type == 'num':
        bars_s = 4
    elif type == 'txt':
        bars_s = 12
    else:
        bars_s = 0
    if (x-bars_s) % 2 != 0:
        x -=1
    bars_text = int(((x-len(text))/2)-1)
    bars = int((x-bars_s)/2-2)
    curses.textpad.rectangle(pad,0,int((x-len(text))/2-1),2,int((x+len(text))/2))
    if len(text) %2 != 0:
        pad.addstr(1,0,'╔'+'═'*(bars_text-1)+'╡'+text+'╞'+'═'*(bars_text)+'╗')
    else:
        pad.addstr(1,0,'╔'+'═'*(bars_text-1)+'╡'+text+'╞'+'═'*(bars_text-1)+'╗')
    for i in range(2,(y-2)):
        pad.addstr(i,0,'║')
        pad.addstr(i,x-1,'║')
    if bars_s != 0:
        pad.addstr((y-2),0,'╚'+'═'*bars+'╣'+' '*bars_s+'╠'+'═'*(bars)+'╝')
        pad.addstr((y-3),bars+1,'╔'+'═'*bars_s+'╗')
        pad.addstr((y-1),bars+1,'╚'+'═'*bars_s+'╝')
    else:
        pad.addstr((y-2),0,'╚'+'═'*(bars+2)+'═'*(bars)+'╝')

def box_inator_duo(pad,text,text2):
    pad.clear()
    y,x = pad.getmaxyx()
    #Crear caja  de texto
    if x % 2 != 0:
        x -=1
    bars_text = int(((x-len(text))/2)-1)
    bars = int((x-len(text2))/2-1)
    curses.textpad.rectangle(pad,0,int((x-len(text))/2-1),2,int((x+len(text))/2))
    curses.textpad.rectangle(pad,(y-3),int((x-len(text2))/2-1),(y-1),int((x+len(text2))/2))
    if len(text) %2 != 0:
        pad.addstr(1,0,'╔'+'═'*(bars_text-1)+'╡'+text+'╞'+'═'*(bars_text)+'╗')
    else:
        pad.addstr(1,0,'╔'+'═'*(bars_text-1)+'╡'+text+'╞'+'═'*(bars_text-1)+'╗')
    for i in range(2,(y-2)):
        pad.addstr(i,0,'║')
        pad.addstr(i,x-1,'║')
    if (len(text2) %2) != 0:
        pad.addstr((y-2),0,'╚'+'═'*(bars-1)+'╡'+text2+'╞'+'═'*(bars)+'╝')
    else:
        pad.addstr((y-2),0,'╚'+'═'*(bars-1)+'╡'+text2+'╞'+'═'*(bars-1)+'╝')

def general_win_border(pad1,pad2,pad3,mit_ancho):
    pad1.box()
    pad2.box()
    pad3.box()
    pad3.addstr(0,int(mit_ancho*0.5-10),'╖ Orden de Combate ╓')
    pad3.addstr(1,int(mit_ancho*0.5-10),'╚══════════════════╝')
    pad1.addstr(0,int(mit_ancho*0.5-4),'╖ Menu ╓')
    pad1.addstr(1,int(mit_ancho*0.5-4),'╚══════╝')
    pad2.addstr(0,int(mit_ancho*0.5-11),'╖ Registro de Combate ╓')
    pad2.addstr(1,int(mit_ancho*0.5-11),'╚═════════════════════╝')
    pad2.refresh()
    pad1.refresh()
    pad2.refresh()
    pad3.refresh()