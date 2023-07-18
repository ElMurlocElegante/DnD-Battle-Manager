
def damage_log(pad):
    pad.clear()
    y,x = pad.getmaxyx()
    file = open('resources\\battle_log.txt',mode='r')
    log = file.readlines()
    if len(log) < y:
        for i in range(len(log)):
            pad.addstr(i,1,log[len(log)-i-1])
    else:
        for i in range(y-1):
            pad.addstr(i,1,log[len(log)-i-1])
    pad.refresh()

def damage_top(pad,df_dmg):
    y,x = pad.getmaxyx()
    df_dmg.loc
    for i in range(y-1):
        try:
            pad.addstr(i,int(x-x*0.4),f'{i+1}-{df_dmg.iloc[i,0]}, con {int(df_dmg.iloc[i,1])} de daño')
        except:
            pad.addstr(i,int(x-x*0.4),' '*int(x*0.4))
    pad.refresh()
def turn_log(ronda):
    file = open('resources\\battle_log.txt',mode='a')
    file.write(f'Ronda N°{ronda}\n')
    file.close()
