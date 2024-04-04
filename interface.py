import time
from main_functions import *
from suport_functions import *
from screen_config import *
from battle_log import *
from main_battle import battle

dead_npc = []
damage_data = pd.DataFrame({'Character':[],'Damage':[]})

inic_pool,damage_data = call_inic_char(left_scr_up,left_scr_up_in,num_win,damage_data,g_b,r_b)

draw_dataframe(right_scr,inic_pool)
left_scr_up.clear()
text_list = ['Agregar un NPC','Eliminar un NPC','Modificar HP de un NPC','Modificar Iniciativa de un NPC','Iniciar Combate']
selec = 0
key = ''
box_inator(left_scr_up_in,'Seleccione una Opción','none')
left_scr_up_in.refresh()

ronda = 1
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
            inic_pool = battle(left_scr_up,left_scr_up_in,left_scr_dw,num_win,text_win,right_scr,left_scr_up_out,left_scr_dw_out,right_scr_out,inic_pool,dead_npc,damage_data,text_list,x,y,g_b,r_b,mit_ancho)
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
    

