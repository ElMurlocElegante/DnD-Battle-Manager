from suport_functions import draw_dataframe,box_inator_duo
from main_functions import call_inic_enemy,menu_scroll,box_inator,death_saving,reaction_mod,del_char,hp_modifier,general_win_border
from battle_log import turn_log,damage_log,damage_top
import time
import curses
def battle(pad,pad_b,pad_d,pad_n,pad_t,pad_df,pad_out,pad_d_out,pad_t_out,df,dead_npc,dmg_data,text_list,x,y,g_b,r_b,mit_ancho):
    ronda = 1
    while True:
        df_temp = df.copy()
        turn_log(ronda)
        for pc in df_temp['Character']:
            damage_log(pad_d)
            damage_top(pad_d,dmg_data)
            while True:
                pad.clear()
                box_inator_duo(pad_b,f'Turno de {pc}',f'Ronda N°{ronda}')
                pad_b.refresh()
                draw_dataframe(pad_df,df)
                if int(df.loc[df['Character']==pc,'HP'].iloc[0])<= 0: # type: ignore
                    if pc in ['Ariel','Gallo','Iago','JF','Logan']:
                        if df_temp.loc[df_temp['Character']==pc,'F'].iloc[0] == 3: # type: ignore
                            pad.addstr(0,int((x-len(f'{pc} Está Muerto'))/2),f'{pc} Está Muerto')
                            pad.refresh()
                            time.sleep(2)
                            break
                        else:
                            df = death_saving(pad,pad_b,pad_n,df,pc,g_b,r_b)
                    else:
                        df, dead_npc = del_char(df,pc,dead_npc)
                        pad_d.clear()
                        pad_d.addstr(0,0,f'{dead_npc}')
                        pad_d.refresh()
                    time.sleep(1)    
                    break
                else:
                    pad.clear()

                    if x % 2 != 0:
                        x -=1
                    text_list_combat = ['Atacar/Curar','Acción de Reacción','Agregar un NPC','Funciones Especiales','Terminar Turno']
                    key = ' '
                    selec = 0
                    while True:
                        if key == 'KEY_UP':
                            selec -= 1
                        elif key == 'KEY_DOWN':
                            selec += 1
                        elif key == '\n':
                            if selec == 0:
                                df,dmg_data = hp_modifier(pad,pad_b,pad_n,df,dmg_data,pc,g_b,r_b)
                                draw_dataframe(pad_df,df)
                                box_inator_duo(pad_b,f'Turno de {pc}',f'Ronda N°{ronda}')
                                damage_log(pad_d)
                                damage_top(pad_d,dmg_data)
                                pad_b.refresh()
                            elif selec == 1:
                                df,dmg_data = reaction_mod(pad,pad_b,pad_n,df,dmg_data,g_b,r_b)
                                draw_dataframe(pad_df,df)
                                box_inator_duo(pad_b,f'Turno de {pc}',f'Ronda N°{ronda}')
                                damage_log(pad_d)
                                damage_top(pad_d,dmg_data)
                                pad_b.refresh()
                            elif selec == 2:
                                df,dmg_data = call_inic_enemy(pad,pad_b,pad_n,pad_t,df,dmg_data,g_b,r_b)
                                draw_dataframe(pad_df,df)
                                box_inator_duo(pad_b,f'Turno de {pc}',f'Ronda N°{ronda}')
                                pad_b.refresh()
                            elif selec == 3:
                                pad.clear()
                                pad.refresh()
                                key = ''
                                selec = 0
                                text_list_2 = ['Scrollear en Tabla','Ver Lista de Enemigos Muertos','Forzar Actualización de Bordes']
                                while True:
                                    if key == 'KEY_UP':
                                        selec -= 1
                                    elif key == 'KEY_DOWN':
                                        selec += 1
                                    elif key == 'q' or key == 'Q':
                                        pad.clear()
                                        break
                                    elif key == '\n':
                                        if selec == 0:
                                            menu_scroll(pad_df,df)
                                            box_inator_duo(pad_b,f'Turno de {pc}',f'Ronda N°{ronda}')
                                            pad_b.refresh()
                                            break
                                        elif selec == 1:
                                            pad.clear()
                                            box_inator(pad_b,'Lista de Enemigos Muertos','none')
                                            pad.addstr(str(dead_npc))
                                            pad_b.refresh()
                                            pad.refresh()
                                            pad.getkey()
                                            box_inator_duo(pad_b,f'Turno de {pc}',f'Ronda N°{ronda}')
                                            pad_b.refresh()
                                            break
                                        elif selec == 2:
                                            general_win_border(pad_out,pad_d_out,pad_t_out,mit_ancho)
                                            box_inator_duo(pad_b,f'Turno de {pc}',f'Ronda N°{ronda}')
                                            pad_b.refresh()
                                            draw_dataframe(pad_df,df)
                                            break
                                    if selec < 0:
                                        selec = 2
                                    elif selec >2:
                                        selec = 0
                                    for i in range(len(text_list_2)):
                                        pad.addstr(i,int((x-len(text_list_2[i]))/2-1),' '+text_list_2[i]+' ')
                                    pad.addstr(selec,int((x-len(text_list_2[selec]))/2-1),'»'+' '*len(text_list_2[selec])+'«')
                                    pad.addstr(selec,int((x-len(text_list_2[selec]))/2),text_list_2[selec],curses.A_STANDOUT)
                                    pad.addstr(y-1,int(x-len('Q para volver al Menú')-2),'Q para volver al Menú')
                                    pad.refresh()
                                    key = pad.getkey()
                                key = ''
                                selec = 0
                                pad.clear

                            elif selec == 4:
                                break                                
                        if selec < 0:
                            selec = 4
                        elif selec >4:
                            selec = 0
                        for i in range(len(text_list)):
                            pad.addstr(i,int((x-len(text_list_combat[i]))/2-1),' '+text_list_combat[i]+' ')
                        pad.addstr(selec,int((x-len(text_list_combat[selec]))/2-1),'»'+' '*len(text_list_combat[selec])+'«')
                        pad.addstr(selec,int((x-len(text_list_combat[selec]))/2),text_list_combat[selec],curses.A_STANDOUT)
                        pad.refresh()
                        key = pad.getkey()
                break
        if (df['S'] >= 0).all():
            pad.clear()
            pad.addstr(int((y-1)/2)-3,int((x-len('Todos los Enemigos están Muertos'))/2),'Todos los Enemigos están Muertos')
            pad.addstr(int((y-1)/2)-2,int((x-len('Desea Terminar el Combate ?'))/2),'Desea Terminar el Combate ?')
            key = ''
            selec = 0
            while True:
                pad.addstr(int((y-1)/2),int(x/2-5),' SI / NO ')
                if key == 'KEY_LEFT':
                    selec -= 1
                elif key == 'KEY_RIGHT':
                    selec += 1
                elif key == '\n':
    
                    if selec == 0:
                        df.sort_values(by='Character').to_csv('resources\\pc_stats.csv',columns=['Character','Max HP','HP','AC'],sep=';',index=False)
                        pad_b.clear()
                        for i in range(4):
                            pad.addstr(int((y-1)/2),int((x-len('Combate Terminado'))/2),'Combate Terminado')
                            pad.refresh()
                            time.sleep(0.1)
                            pad.addstr(int((y-1)/2),int((x-len('Combate Terminado'))/2),'Combate Terminado', curses.A_STANDOUT)
                            pad.refresh()
                            time.sleep(0.1)
                        time.sleep(0.5)
                        box_inator(pad_b,'Seleccione una Opción','none')
                        pad_b.refresh()
                        draw_dataframe(pad_df,df)
                        return df
                    else:
                        pad.clear()
                        ronda += 1
                        break
                if selec < 0:
                    selec = 1
                elif selec > 1:
                    selec = 0
                if selec == 0:
                    pad.addstr(int((y-1)/2),int(x/2-5),'»SI«')
                    pad.addstr(int((y-1)/2),int(x/2-4),'SI',curses.A_STANDOUT)
                elif selec == 1:
                    pad.addstr(int((y-1)/2),int(x/2),'»NO«')
                    pad.addstr(int((y-1)/2),int(x/2)+1,'NO',curses.A_STANDOUT)
                pad.refresh()
                key = pad.getkey()

        else:
            ronda +=1