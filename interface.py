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
text_list = ['Agregar un NPC','Eliminar un NPC','Modificar HP de un NPC','Iniciar Combate']
selec = 0
key = ''
box_inator(left_scr_up_in,'Seleccione una Opción','num')
left_scr_up_in.refresh()
while True:

    if key == 'KEY_UP':
        selec -= 1
    elif key == 'KEY_DOWN':
        selec += 1
    elif key == '\n':
        if selec == 0:
            inic_pool = call_inic_enemy(left_scr_up,left_scr_up_in,num_win,text_win,inic_pool,g_b,r_b)
            draw_dataframe(right_scr,inic_pool)
            box_inator(left_scr_up_in,'Seleccione una Opción','num')
            left_scr_up_in.refresh()
        elif selec == 1:
            inic_pool = call_inic_del(left_scr_up,left_scr_up_in,inic_pool)
            draw_dataframe(right_scr,inic_pool)
            box_inator(left_scr_up_in,'Seleccione una Opción','num')
            left_scr_up_in.refresh()
        elif selec == 2:
            inic_pool = hp_modifier(left_scr_up,left_scr_up_in,num_win,inic_pool,g_b,r_b)
            draw_dataframe(right_scr,inic_pool)
            box_inator(left_scr_up_in,'Seleccione una Opción','num')
            left_scr_up_in.refresh()
        elif selec == 3:
            break
    if selec < 0:
        selec = 3
    elif selec >3:
        selec = 0
    for i in range(len(text_list)):
        left_scr_up.addstr(i,int((x-(len(text_list[i])))/2)-1,' '+text_list[i]+' ')
    left_scr_up.addstr(selec,int((x-(len(text_list[selec])))/2)-1,'»'+text_list[selec]+'«')
    left_scr_up.addstr(selec,int((x-(len(text_list[selec])))/2),text_list[selec],curses.A_STANDOUT)

    left_scr_up.refresh()
    
    key = left_scr_up.getkey()


ronda = 1
while True:
    inic_pool_temp = inic_pool.copy()
    for pc in inic_pool_temp['Character']:
        while True:
            left_scr_up.clear()
            box_inator_duo(left_scr_up_in,f'Turno de {pc}',f'Ronda N°{ronda}')
            left_scr_up_in.refresh()
            draw_dataframe(right_scr,inic_pool)
            if int(inic_pool.loc[inic_pool['Character']==pc,'HP'].iloc[0])<= 0: # type: ignore
                if pc in ['Ariel','Gallo','Iago','JF','Logan']:
                    if inic_pool_temp.loc[inic_pool_temp['Character']==pc,'Failure'].iloc[0] == 3: # type: ignore
                        left_scr_up.addstr(0,int((x-len(f'{pc} Está Muerto'))/2),f'{pc} Está Muerto')
                        left_scr_up.refresh()
                        time.sleep(2)
                        break
                    else:
                        inic_pool = death_saving(left_scr_up,left_scr_up_in,num_win,inic_pool,pc,g_b,r_b)
                if pc not in ['Ariel','Gallo','Iago','JF','Logan']:
                    if pc not in death_npc['Character'].values:
                        inic_pool, death_npc = del_char(inic_pool,pc,death_npc)
                        left_scr_dw.clear()
                        left_scr_dw.addstr(0,0,f'{death_npc["Character"].tolist()}')
                        left_scr_dw.refresh()
                time.sleep(1)    
                break
            else:
                left_scr_up.clear()
                
                if x % 2 != 0:
                    x -=1
                text_list = ['Atacar/Curar','Agregar un NPC','Forzar Actualización de Bordes','Terminar Turno']
                key = ' '
                selec = 0
                while True:

                    if key == 'KEY_UP':
                        selec -= 1
                    elif key == 'KEY_DOWN':
                        selec += 1
                    elif key == '\n':
                        if selec == 0:
                            inic_pool = hp_modifier(left_scr_up,left_scr_up_in,num_win,inic_pool,g_b,r_b)
                            draw_dataframe(right_scr,inic_pool)
                            box_inator_duo(left_scr_up_in,f'Turno de {pc}',f'Ronda N°{ronda}')
                            left_scr_up_in.refresh()
                        elif selec == 1:
                            inic_pool = call_inic_enemy(left_scr_up,left_scr_up_in,num_win,text_win,inic_pool,g_b,r_b)
                            draw_dataframe(right_scr,inic_pool)
                            box_inator_duo(left_scr_up_in,f'Turno de {pc}',f'Ronda N°{ronda}')
                            left_scr_up_in.refresh()
                        elif selec == 2:
                            general_win_border(left_scr_up_out,left_scr_dw_out,right_scr_out,mit_ancho)
                            box_inator_duo(left_scr_up_in,f'Turno de {pc}',f'Ronda N°{ronda}')
                            left_scr_up_in.refresh()
                            draw_dataframe(right_scr,inic_pool)
                            
                        elif selec == 3:
                            break                                
                    if selec < 0:
                        selec = 3
                    elif selec >3:
                        selec = 0
                    for i in range(len(text_list)):
                        left_scr_up.addstr(i,int((x-len(text_list[i]))/2-1),' '+text_list[i]+' ')
                    left_scr_up.addstr(selec,int((x-len(text_list[selec]))/2-1),'»'+' '*len(text_list[selec])+'«')
                    left_scr_up.addstr(selec,int((x-len(text_list[selec]))/2),text_list[selec],curses.A_STANDOUT)
                    left_scr_up.refresh()
                    key = left_scr_up.getkey()
            break
    ronda +=1

