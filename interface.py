import time
from main_functions import *
from suport_functions import *
from screen_config import *
from battle_log import *

pc_data = read_pc_data()
death_npc = []
damage_data = pd.DataFrame({'Character':[],'Damage':[]})

inic_pool,damage_data = call_inic_char(left_scr_up,left_scr_up_in,num_win,pc_data,damage_data,g_b,r_b)

draw_dataframe(right_scr,inic_pool)
left_scr_up.clear()
text_list = ['Agregar un NPC','Eliminar un NPC','Modificar HP de un NPC','Modificar Iniciativa de un NPC','Iniciar Combate']
selec = 0
key = ''
box_inator(left_scr_up_in,'Seleccione una Opción','none')
left_scr_up_in.refresh()
while True:

    if key == 'KEY_UP':
        selec -= 1
    elif key == 'KEY_DOWN':
        selec += 1
    elif key == '\n':
        if selec == 0:
            inic_pool,damage_data = call_inic_enemy(left_scr_up,left_scr_up_in,num_win,text_win,inic_pool,damage_data,g_b,r_b)
            draw_dataframe(right_scr,inic_pool)
            box_inator(left_scr_up_in,'Seleccione una Opción','none')
            left_scr_up_in.refresh()
        elif selec == 1:
            inic_pool = call_inic_del(left_scr_up,left_scr_up_in,inic_pool)
            draw_dataframe(right_scr,inic_pool)
            box_inator(left_scr_up_in,'Seleccione una Opción','none')
            left_scr_up_in.refresh()
        elif selec == 2:
            inic_pool,damage_data = hp_modifier(left_scr_up,left_scr_up_in,num_win,inic_pool,damage_data,'system',g_b,r_b)
            draw_dataframe(right_scr,inic_pool)
            box_inator(left_scr_up_in,'Seleccione una Opción','none')
            left_scr_up_in.refresh()
        elif selec == 3:
            inic_pool = inic_modifier(left_scr_up,left_scr_up_in,num_win,inic_pool,g_b,r_b)
            draw_dataframe(right_scr,inic_pool)
            box_inator(left_scr_up_in,'Seleccione una Opción','none')
            left_scr_up_in.refresh()
        elif selec == 4:
            break
    if selec < 0:
        selec = 4
    elif selec >4:
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
    turn_log(ronda)
    for pc in inic_pool_temp['Character']:
        damage_log(left_scr_dw)
        damage_top(left_scr_dw,damage_data)
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
                    if pc not in death_npc:
                        inic_pool, death_npc = del_char(inic_pool,pc,death_npc)
                        left_scr_dw.clear()
                        left_scr_dw.addstr(0,0,f'{death_npc}')
                        left_scr_dw.refresh()
                time.sleep(1)    
                break
            else:
                left_scr_up.clear()
                
                if x % 2 != 0:
                    x -=1
                text_list = ['Atacar/Curar','Acción de Reacción','Agregar un NPC','Funciones Especiales','Terminar Turno']
                key = ' '
                selec = 0
                while True:

                    if key == 'KEY_UP':
                        selec -= 1
                    elif key == 'KEY_DOWN':
                        selec += 1
                    elif key == '\n':
                        if selec == 0:
                            inic_pool,damage_data = hp_modifier(left_scr_up,left_scr_up_in,num_win,inic_pool,damage_data,pc,g_b,r_b)
                            draw_dataframe(right_scr,inic_pool)
                            box_inator_duo(left_scr_up_in,f'Turno de {pc}',f'Ronda N°{ronda}')
                            damage_log(left_scr_dw)
                            damage_top(left_scr_dw,damage_data)
                            left_scr_up_in.refresh()
                        elif selec == 1:
                            inic_pool,damage_data = reaction_mod(left_scr_up,left_scr_up_in,num_win,inic_pool,damage_data,g_b,r_b)
                            draw_dataframe(right_scr,inic_pool)
                            box_inator_duo(left_scr_up_in,f'Turno de {pc}',f'Ronda N°{ronda}')
                            damage_log(left_scr_dw)
                            damage_top(left_scr_dw,damage_data)
                            left_scr_up_in.refresh()
                        elif selec == 2:
                            inic_pool,damage_data = call_inic_enemy(left_scr_up,left_scr_up_in,num_win,text_win,inic_pool,damage_data,g_b,r_b)
                            draw_dataframe(right_scr,inic_pool)
                            box_inator_duo(left_scr_up_in,f'Turno de {pc}',f'Ronda N°{ronda}')
                            left_scr_up_in.refresh()
                        elif selec == 3:
                            left_scr_up.clear()
                            left_scr_up.refresh()
                            key = ''
                            selec = 0
                            text_list_2 = ['Scrollear en Tabla','Ver Lista de Enemigos Muertos','Forzar Actualización de Bordes']
                            while True:
                                if key == 'KEY_UP':
                                    selec -= 1
                                elif key == 'KEY_DOWN':
                                    selec += 1
                                elif key == 'q' or key == 'Q':
                                    break
                                elif key == '\n':
                                    if selec == 0:
                                        menu_scroll(right_scr,inic_pool)
                                        break
                                    elif selec == 1:
                                        left_scr_up.clear()
                                        box_inator(left_scr_up_in,'Lista de Enemigos Muertos','none')
                                        left_scr_up.addstr(str(death_npc))
                                        left_scr_up_in.refresh()
                                        left_scr_up.refresh
                                        left_scr_up.getkey()
                                        box_inator_duo(left_scr_up_in,f'Turno de {pc}',f'Ronda N°{ronda}')
                                        left_scr_up_in.refresh()
                                        break
                                    elif selec == 2:
                                        general_win_border(left_scr_up_out,left_scr_dw_out,right_scr_out,mit_ancho)
                                        box_inator_duo(left_scr_up_in,f'Turno de {pc}',f'Ronda N°{ronda}')
                                        left_scr_up_in.refresh()
                                        draw_dataframe(right_scr,inic_pool)
                                        break
                                if selec < 0:
                                    selec = 2
                                elif selec >2:
                                    selec = 0
                                for i in range(len(text_list_2)):
                                    left_scr_up.addstr(i,int((x-len(text_list_2[i]))/2-1),' '+text_list_2[i]+' ')
                                left_scr_up.addstr(selec,int((x-len(text_list_2[selec]))/2-1),'»'+' '*len(text_list_2[selec])+'«')
                                left_scr_up.addstr(selec,int((x-len(text_list_2[selec]))/2),text_list_2[selec],curses.A_STANDOUT)
                                left_scr_up.addstr(y-1,int(x-len('Q para volver al Menú')-2),'Q para volver al Menú')
                                left_scr_up.refresh()
                                key = left_scr_up.getkey()
                            key = ''
                            selec = 0
                            left_scr_up.clear()

                            
                        elif selec == 4:
                            break                                
                    if selec < 0:
                        selec = 4
                    elif selec >4:
                        selec = 0
                    for i in range(len(text_list)):
                        left_scr_up.addstr(i,int((x-len(text_list[i]))/2-1),' '+text_list[i]+' ')
                    left_scr_up.addstr(selec,int((x-len(text_list[selec]))/2-1),'»'+' '*len(text_list[selec])+'«')
                    left_scr_up.addstr(selec,int((x-len(text_list[selec]))/2),text_list[selec],curses.A_STANDOUT)
                    left_scr_up.refresh()
                    key = left_scr_up.getkey()
            break
    ronda +=1

