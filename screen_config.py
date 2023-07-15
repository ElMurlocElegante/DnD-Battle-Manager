import curses

stdscr=curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
alto,ancho = stdscr.getmaxyx()
marg_sup = int(alto*0.1)
marg_lat = int(ancho*0.1)

'''
curses.textpad.rectangle(win, uly, ulx, lry, lrx)
curses.newwin(nlines, ncols, begin_y, begin_x)
 '''
#Calculo de Dimensiones
mit_alto = int((alto-marg_sup*2)*0.5)
mit_ancho = int((ancho-marg_lat*2)*0.5)



#Ventanas-Bordes
left_scr_up_out = curses.newwin(mit_alto,mit_ancho,(marg_sup),(marg_lat))
left_scr_dw_out = curses.newwin(mit_alto,mit_ancho,(marg_sup+mit_alto),marg_lat)
right_scr_out = curses.newwin((alto-marg_sup*2),mit_ancho,marg_sup,(mit_ancho + marg_lat+1))
#Ventanas-Bordes Interiores
left_scr_up_in = curses.newwin((mit_alto-3),(mit_ancho-2),(marg_sup+2),(marg_lat+1))
left_scr_dw_in = curses.newwin((mit_alto-3),(mit_ancho-2),(marg_sup+mit_alto+2),(marg_lat+1))
#Ventanas-General
left_scr_up = curses.newwin((mit_alto-9),(mit_ancho-4),(marg_sup+5),(marg_lat+2))
left_scr_dw = curses.newwin((mit_alto-9),(mit_ancho-4),(marg_sup+mit_alto+5),(marg_lat+2))
right_scr = curses.newwin((alto-marg_sup*2-3),(mit_ancho-2),(marg_sup+2),(mit_ancho + marg_lat + 2))
text_win = curses.newwin(1, 12, (marg_sup+14), int(marg_lat+mit_ancho*0.5-6))
num_win = curses.newwin(1, 4, (marg_sup+14), int(marg_lat+mit_ancho*0.5-2))
#Flavor
left_scr_up.keypad(True)
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
curses.init_pair(1 ,curses.COLOR_GREEN,curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
r_b = curses.color_pair(2)
g_b = curses.color_pair(1)
y,x=left_scr_up.getmaxyx()