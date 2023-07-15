from curses.textpad import rectangle,Textbox
from main_functions import *
from suport_functions import *
from screen_config import *

pc_data = read_pc_data()
death_npc = pd.DataFrame({'Character':[]})

inic_pool = call_inic_char(left_scr_up,left_scr_up_in,num_win,pc_data,g_b,r_b)

action = ''
draw_dataframe(right_scr,inic_pool)
left_scr_up.clear()

selec = 0
key = ' '
while True:
    box_inator(left_scr_up_in,'Seleccione una Opción','num')
    if key == 'KEY_UP':
        selec -= 1
    elif key == 'KEY_DOWN':
        selec += 1
    elif key == '\n':
        if selec == 0:
            inic_pool = call_inic_enemy(left_scr_up,left_scr_up_in,num_win,text_win,inic_pool,g_b,r_b)
            draw_dataframe(right_scr,inic_pool)
        elif selec == 1:
            inic_pool = call_inic_del(left_scr_up,inic_pool,marg_sup,marg_lat)
            draw_dataframe(right_scr,inic_pool)
        elif selec == 2:
            inic_pool = hp_modifier(left_scr_up,inic_pool,marg_sup,marg_lat)
            draw_dataframe(right_scr,inic_pool)
        elif selec == 3:
            break
    if selec < 0:
        selec = 3
    elif selec >3:
        selec = 0
    if selec == 0:
        left_scr_up.addstr(0,int(x/2-8),'»'+' '*14+'«')
        left_scr_up.addstr(0,int(x/2-7),'Agregar un NPC',curses.A_STANDOUT)
        left_scr_up.addstr(1,int(x/2-8),' Eliminar un NPC ')
        left_scr_up.addstr(2,int(x/2-12),' Modificar HP de un NPC ')
        left_scr_up.addstr(3,int(x/2-8),' Iniciar Combate ') 
    elif selec == 1:
        left_scr_up.addstr(1,int(x/2-8),'»'+' '*15+'«')
        left_scr_up.addstr(0,int(x/2-8),' Agregar un NPC ')
        left_scr_up.addstr(1,int(x/2-7),'Eliminar un NPC',curses.A_STANDOUT)
        left_scr_up.addstr(2,int(x/2-12),' Modificar HP de un NPC ')
        left_scr_up.addstr(3,int(x/2-8),' Iniciar Combate ') 
    elif selec == 2:
        left_scr_up.addstr(2,int(x/2-11),'»'+' '*12+'«')
        left_scr_up.addstr(0,int(x/2-8),' Agregar un NPC ')
        left_scr_up.addstr(1,int(x/2-8),' Eliminar un NPC ')
        left_scr_up.addstr(2,int(x/2-11),'Modificar HP de un NPC',curses.A_STANDOUT)
        left_scr_up.addstr(3,int(x/2-8),' Iniciar Combate ') 
    elif selec == 3:
        left_scr_up.addstr(2,int(x/2-8),'»'+' '*15+'«')
        left_scr_up.addstr(0,int(x/2-8),' Agregar un NPC ')
        left_scr_up.addstr(1,int(x/2-8),' Eliminar un NPC ')
        left_scr_up.addstr(2,int(x/2-12),' Modificar HP de un NPC ')
        left_scr_up.addstr(3,int(x/2-7),'Iniciar Combate',curses.A_STANDOUT)
    left_scr_up.refresh()
    key = left_scr_up.getkey()


ronda = 0
while True:
    inic_pool_temp = inic_pool.copy()
    for pc in inic_pool_temp['Character']:
        while True:
            left_scr_up.clear()
            text_ronda = f'Ronda N°{ronda}'
            slow_print(left_scr_up,f'{"-"*15}Ronda N°{ronda}{"-"*15}',0.005)
            draw_dataframe(right_scr,inic_pool)
            text_turno = f'Turno de {pc}'
            slow_print(text_win,f'{"-"*int((len(text_ronda)+30-len(text_turno))/2)}{text_turno}{"-"*int((len(text_ronda)+30-len(text_turno))/2)}',0.01)
            if int(inic_pool.loc[inic_pool['Character']==pc,'HP'].iloc[0])<= 0: # type: ignore
                if pc in ['Ariel','Gallo','Iago','JF','Logan']:
                    if inic_pool_temp.loc[inic_pool_temp['Character']==pc,'Failure'].iloc[0] == 3: # type: ignore
                        slow_print(text_win,f'\n{pc} Esta Muerto',0.02)
                        time.sleep(2)
                        break
                    inic_pool = death_saving(text_win,left_scr_up,inic_pool,pc,marg_sup,marg_lat)
                if pc not in ['Ariel','Gallo','Iago','JF','Logan']:
                    if pc not in death_npc['Character'].values:
                        inic_pool, death_npc = del_char(inic_pool,pc,death_npc)
                        left_scr_dw.clear()
                        slow_print(left_scr_dw,f'{"-"*15}Lista de Enemigos Muertos{"-"*15}\n{death_npc["Character"].tolist()}',0.01)
                time.sleep(1)    
                break
            else:
                slow_print(text_win,'\nSeleccione una acción:\n(1)Atacar/Curar\n(2)Agregar un NPC\n(3)Terminar turno',0.005)
                rectangle(left_scr_up, 7, 3, 9, 16)
                num_win = curses.newwin(1, 3, (marg_sup+10), (marg_lat+10))
                left_scr_up.refresh()
                box = Textbox(num_win)
                try:   
                    box.edit()
                    action = int(box.gather())
                except ValueError:
                    slow_print(text_win,'\nERROR, Ingrese un número',0.01)
                    text_win.getch()
                    continue
                if action == 1:
                    inic_pool = hp_modifier(left_scr_up,inic_pool,marg_sup,marg_lat)
                elif action == 2:
                    inic_pool = call_inic_enemy(left_scr_up,left_scr_up_in,num_win,text_win,inic_pool,g_b,r_b)
                elif action == 3:
                    break
    ronda +=1

