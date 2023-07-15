import random
from tabulate import tabulate
import pandas as pd
import time
import curses.textpad

def get_input_data(pad,pad_n,x,y,col1,col2):
    box = curses.textpad.Textbox(pad_n)
    while True:
        box.edit()
        try:
            input_data = int(box.gather())
            pad.addstr(y,int(x-x*0.1)-1," "*4)
            pad.addstr(y,int(x-x*0.1)-1,str(input_data),col1)
            pad_n.clear()
            pad.refresh()
            pad_n.refresh()
            return input_data
        except ValueError:
            input_data = box.gather()
            pad.addstr(y,int(x-x*0.1)-1,str(input_data),col2)
            pad_n.clear()
            pad_n.refresh()
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

def get_input_data_txt(pad,pad_t,x,y,col1,col2):
    box = curses.textpad.Textbox(pad_t)
    while True:
        box.edit()
        input_data = box.gather()
        pad.addstr(y,int(x-x*0.1-6)," "*12)
        pad.addstr(y,int(x-x*0.1-6),str(input_data),col1)
        pad_t.clear()
        pad.refresh()
        pad_t.refresh()
        return input_data



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

def box_inator(pad,text,type):
    pad.clear()
    y,x = pad.getmaxyx()
    #Crear caja  de texto
    bars_text = int(((x-len(text))/2)-1)
    bars_s = 0
    if type == 'num':
        bars_s = 4
    elif type == 'txt':
        bars_s = 12
    if (x-bars_s) % 2 != 0:
        x -=1
    bars = int((x-bars_s)/2-2)
    curses.textpad.rectangle(pad,0,int((x-len(text))/2-1),2,int((x+len(text))/2))
    if (bars_text) %2 != 0:
        pad.addstr(1,0,'╔'+'═'*(bars_text-1)+'╡'+text+'╞'+'═'*bars_text+'╗')
    else:
        pad.addstr(1,0,'╔'+'═'*(bars_text-2)+'╡'+text+'╞'+'═'*bars_text+'╗')
    for i in range(2,(y-2)):
        pad.addstr(i,0,'║')
        pad.addstr(i,x,'║')
    pad.addstr((y-2),0,'╚'+'═'*bars+'╣'+' '*bars_s+'╠'+'═'*(bars+1)+'╝')
    pad.addstr((y-3),bars+1,'╔'+'═'*bars_s+'╗')
    pad.addstr((y-1),bars+1,'╚'+'═'*bars_s+'╝')
    