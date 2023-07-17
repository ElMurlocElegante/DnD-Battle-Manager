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
        input_data = input_data.strip()
        pad.addstr(y,int(x-x*0.1-6)," "*12)
        pad.addstr(y,int(x-x*0.1-6),str(input_data),col1)
        pad_t.clear()
        pad.refresh()
        pad_t.refresh()
        return input_data

def multi_page_menu(pad,pad_b,df,text):
    pad.clear()
    y,x = pad.getmaxyx()
    box_inator(pad_b,text,'none')
    ch_list = df['Character'].tolist()
    selec = 0
    real_selec = 0
    page = 0
    max_page = int(len(ch_list)/y)
    max_selec = len(ch_list)
    
    key = ''
    while True:
        
        if key == 'KEY_UP':
            selec -= 1
            real_selec -= 1
        elif key == 'KEY_DOWN':
            selec += 1
            real_selec +=1
        elif key == 'KEY_LEFT':
            page -=1
            pad.clear()
        elif key == 'KEY_RIGHT':
            page +=1
            pad.clear()
        elif key == '\n':
            key = ''
            pad.addstr(int((y-1)/2),int(x/2-7),'Estas Seguro ?')
            while True:
                pad.addstr(int((y-1)/2)+1,int(x/2-5),' SI / NO ')
                if key == 'KEY_LEFT':
                    real_selec -= 1
                elif key == 'KEY_RIGHT':
                    real_selec += 1
                elif key == '\n':
    
                    if real_selec == 0:
                        return selec+page*(y-2)
                    else:
                        pad.addstr(int((y-1)/2),int(x/2-7),' '*14)
                        pad.addstr(int((y-1)/2)+1,int(x/2-5),' '*9)
                        break
                if real_selec < 0:
                    real_selec = 1
                elif real_selec > 1:
                    real_selec = 0
                if real_selec == 0:
                    pad.addstr(int((y-1)/2)+1,int(x/2-5),'»SI«')
                    pad.addstr(int((y-1)/2)+1,int(x/2-4),'SI',curses.A_STANDOUT)
                elif real_selec == 1:
                    pad.addstr(int((y-1)/2)+1,int(x/2),'»NO«')
                    pad.addstr(int((y-1)/2)+1,int(x/2)+1,'NO',curses.A_STANDOUT)
                pad.refresh()
                key = pad.getkey()

        if selec <0:
            selec = y-2
            page -=1
            pad.clear()
        elif selec > (y-2):
            selec = 0
            page +=1
            pad.clear()
        if (selec + page*(y-2)) >(max_selec-1):
            selec = 0
            page = 0
            pad.clear()
        if page < 0:
            page = int(max_page)
        elif page > max_page:
            page = 0
        for i in range(y-1):
            c = i+page*(y-2)
            try:
                pad.addstr(i,int(x*0.1-1),' '+str(ch_list[c])+' ')
            except:
                pad.addstr(i,int(x*0.1-1),' '*14)
        try:
            pad.addstr(selec,int(x*0.1)-1,'»'+' '*len(ch_list[selec+page*(y-2)])+'«')
            pad.addstr(selec,int(x*0.1),ch_list[selec+page*(y-2)],curses.A_STANDOUT)
        except:
            selec = (max_selec-max_page*(y-2))-1
            pad.addstr(selec,int(x*0.1)-1,'»'+' '*len(ch_list[selec+page*(y-2)])+'«')
            pad.addstr(selec,int(x*0.1),ch_list[selec+page*(y-2)],curses.A_STANDOUT)
        if max_page != 0:
            pad.addstr(y-1,int(x/2-5),f'Página {page}/{max_page}')
        pad_b.refresh()
        pad.refresh()
        key = pad.getkey()


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
    pad3.addstr(0,int(mit_ancho*0.5-9),'╖Orden de Combate╓')
    pad3.addstr(1,int(mit_ancho*0.5-9),'╚════════════════╝')
    pad1.addstr(0,int(mit_ancho*0.5-3),'╖Menu╓')
    pad1.addstr(1,int(mit_ancho*0.5-3),'╚════╝')
    pad2.addstr(0,int(mit_ancho*0.5-9),'╖Enemigos Muertos╓')
    pad2.addstr(1,int(mit_ancho*0.5-9),'╚════════════════╝')
    pad2.refresh()
    pad1.refresh()
    pad2.refresh()
    pad3.refresh()