import curses
import curses.textpad
import time
from suport_functions import box_inator,draw_dataframe

def menu_scroll(pad,df):
    pad.clear()
    y,x = pad.getmaxyx()
    key = ''
    p = 0
    while True:
        if key == 'KEY_UP':
            p -= 1
        elif key == 'KEY_DOWN':
            p += 1      
        elif key == 'q' or key == 'Q':
            break
        if p < 0:
            p = len(df['Character'])-1
        elif p > len(df['Character'])-1:
            p = 0
        draw_dataframe(pad,df.loc[p:p+y])

        key = pad.getkey()
        
def menu(pad,df):
    pad.clear()
    y,x = pad.getmaxyx()
    multi_page_menu(pad,None,df,None)

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
    if pad_b != None:
        box_inator(pad_b,text,'none')
    ch_list = df.iloc[:,0].tolist()
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
        elif key == 'q' or key == 'Q':
            return 'q'
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
        pad.addstr(y-1,int(x-len('Q para volver al Menú')-2),'Q para volver al Menú')
        try:
            pad.addstr(selec,int(x*0.1)-1,'»'+' '*len(ch_list[selec+page*(y-2)])+'«')
            pad.addstr(selec,int(x*0.1),ch_list[selec+page*(y-2)],curses.A_STANDOUT)
        except:
            selec = (max_selec-max_page*(y-2))-1
            pad.addstr(selec,int(x*0.1)-1,'»'+' '*len(ch_list[selec+page*(y-2)])+'«')
            pad.addstr(selec,int(x*0.1),ch_list[selec+page*(y-2)],curses.A_STANDOUT)
        if max_page != 0:
            pad.addstr(y-1,int(x/2-5),f'Página {page}/{max_page}')
        if pad_b != None:
            pad_b.refresh()
        pad.refresh()
        key = pad.getkey()
