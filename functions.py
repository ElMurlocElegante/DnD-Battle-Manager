import time
import pandas as pd
import random

def slow_print(text,speed):
    s=' '
    for char in text:
        print(char,end='',flush=True)
        time.sleep(speed)
    return s
def die_gen(die,quant,mod):
    result = 0
    for tirada in range(quant):
        result += random.randint(1,die)
        result += mod
    return result
def tablenator(item):
    item = item.strip('\n')
    item = item.split(';') 
    return item
def inic_call_char(inic_pool,df_c_data):
    PC = {'Character':['Ariel','JF','Gallo','Iago','Logan'],'Iniciativa':[],'Vida':[]}
    for i in range(5):
        while True:
            try:
                inic = int(input(slow_print(f'Ingrese la Iniciativa de {PC["Character"][i]}',0.005)))
                break
            except ValueError:
                print(f'ERROR, Ingrese un número')
        
        PC['Iniciativa'].append(inic)
        PC['Vida'].append(df_c_data['HP'][i])
    c_data = pd.DataFrame(PC)
    inic_pool = pd.concat([inic_pool,c_data],ignore_index=True)
    inic_pool = inic_pool.sort_values('Iniciativa',ascending = False)
    inic_pool = inic_pool.reset_index(drop=True)    
    return inic_pool
def inic_call_enemy(inic_pool):  
    inic_enemigos ={'Character':[],'Iniciativa':[],'Vida':[]}
    while True:
        try:
            enemy_inic = int(input(slow_print('Ingrese el modificador de Dex del enemigo:\n',0.01)))
            enemy_hp_die_q = int(input(slow_print('Ingrese la cantidad de dados a tirar para la vida:\n',0.01)))
            enemy_hp_die = int(input(slow_print('Ingrese el dado a tirar:\n',0.01)))
            enemy_hp_con = int(input(slow_print('Ingrese el modificador de Constitución del enemigo:\n',0.01)))
            break
        except ValueError:
            print('ERROR, Ingrese un número')
    enemy_inic += random.randint(1,20)
    enemy_name = input(slow_print('\nIngrese bajo que nombre será registrado el enemigo: ',0.01))
    enemy_hp = die_gen(enemy_hp_die,enemy_hp_die_q,enemy_hp_con)
    inic_enemigos['Character'].append(enemy_name)
    inic_enemigos['Iniciativa'].append(enemy_inic)
    inic_enemigos['Vida'].append(enemy_hp)
    c_data = pd.DataFrame(inic_enemigos)
    inic_pool = pd.concat([inic_pool,c_data],ignore_index=True)
    inic_pool = inic_pool.sort_values('Iniciativa',ascending = False)
    inic_pool = inic_pool.reset_index(drop=True)      
    return inic_pool
def inic_call_delete(inic_pool):
    print(inic_pool)
    while True:
        try:
            del_char = int(input(slow_print('Ingrese el Número(izquierda) del personaje que desea eliminar',0.01)))
            break
        except ValueError:
            print('ERROR, Ingrese un número')
    inic_pool = inic_pool.drop([del_char])
    inic_pool = inic_pool.sort_values('Iniciativa',ascending = False)
    inic_pool = inic_pool.reset_index(drop=True)    
    return inic_pool
def hp_modifier(inic_pool):
    print(inic_pool)
    while True:
        try:
            selec = int(input(slow_print('Ingrese el índice del personaje a alterar:',0.01)))
            hp_mod = int(input(slow_print('Ingrese la vida a substraer o agregar (con un menos adelante)',0.01)))
            break
        except ValueError:
            print('ERROR, Ingrese un número')
        if selec < 0 or selec>(len(inic_pool)):
            print('ERROR, Ingrese un valor válido')
            return inic_pool
    inic_pool['Vida'][selec]=(int(inic_pool['Vida'][selec]) - hp_mod)
    inic_pool = inic_pool.sort_values('Iniciativa',ascending = False)
    inic_pool = inic_pool.reset_index(drop=True)    
    slow_print('Valores Actualizados.',0.02)
    print(inic_pool)
    return inic_pool
def read_pc_data():
    pc_data = open('pc_stats.csv','r+')
    death_saving = {'Character':[],'Failure':[],'Succes':[]}
    pc_stats = pc_data.readlines()
    pc_data.close()
    pc_stats = list(map(tablenator,pc_stats))
    c_data_stats={'Character':[],'HP':[],'AC':[],'Str':[],'Dex':[],'Con':[],'Int':[],'Wis':[],'Chr':[]}
    pc_stats.pop(0)
    for item in pc_stats:
        for i in range(9):
            key = list(c_data_stats.keys())[i]
            c_data_stats[key].append(item[i])
        death_saving['Character'].append(item[0])
        death_saving['Failure'].append(0)
        death_saving['Succes'].append(0)
    df_c_data = pd.DataFrame(c_data_stats)
    death_saving = pd.DataFrame(death_saving)
    return df_c_data, death_saving
def death_saving_sort(death_saving,inic_pool):
    death_saving = death_saving.merge(inic_pool[['Character','Iniciativa']], on='Character')
    death_saving = death_saving.sort_values(by='Iniciativa', ascending=False)
    death_saving = death_saving.drop('Iniciativa', axis=1)
    death_saving = death_saving.reset_index(drop=True)
    return death_saving
def death_saving_throw(death_saving, inic_pool, turno_name):
    while True:
        try:
            result = int(input(slow_print(f'\n{death_saving.loc[death_saving["Character"] == turno_name, "Character"].iloc[0]} está abatido. Ingrese el resultado del tiro de salvación del jugador', 0.01)))
            if result < 1 or result > 20:
                continue
            else:
                break
        except ValueError:
            print('ERROR, Ingrese un número')
    if result == 1:
        death_saving.loc[death_saving['Character'] == turno_name, 'Failure'] += 2
    elif result in range(2, 10):
        death_saving.loc[death_saving['Character'] == turno_name, 'Failure'] += 1
    elif result in range(10, 19):
        death_saving.loc[death_saving['Character'] == turno_name, 'Succes'] += 1
    elif result == 20:
        death_saving.loc[death_saving['Character'] == turno_name, 'Succes'] = 3
        death_saving.loc[death_saving['Character'] == turno_name, 'Failure'] = 0

    if death_saving.loc[death_saving['Character'] == turno_name, 'Succes'].iloc[0] == 3:
        slow_print('\nEl Personaje logró todos los tiros de salvación.\n', 0.01)
        death_saving.loc[death_saving['Character'] == turno_name, 'Succes'] = 0
        death_saving.loc[death_saving['Character'] == turno_name, 'Failure'] = 0
        inic_pool.loc[inic_pool['Character'] == turno_name, 'Vida'] = '1'
    elif death_saving.loc[death_saving['Character'] == turno_name, 'Failure'].iloc[0] >= 3:
        slow_print('\nEl Personaje muere.\n', 0.01)
    else:
        slow_print(f'\nEl Personaje tiene {death_saving.loc[death_saving["Character"] == turno_name, "Succes"].iloc[0]} tiradas logradas y {death_saving.loc[death_saving["Character"] == turno_name, "Failure"].iloc[0]} tiradas falladas\n', 0.01)
    return death_saving, inic_pool