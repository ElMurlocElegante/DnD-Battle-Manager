import time
import pandas as pd
import random
#Impirimir texto de forma progresiva
def slow_print(text,speed):
    s=' '
    for char in text:
        print(char,end='',flush=True)
        time.sleep(speed)
    return s

#Tirada de Dados
def die_gen(die,quant,mod):
    result = 0
    for tirada in range(quant):
        result += random.randint(1,die)
        result += mod
    return result

#CSV --> Tabla
def tablenator(item):
    item = item.strip('\n')
    item = item.split(';') 
    return item

#Crear PC
def inic_call_char(inic_pool,df_c_data):
    PC = {'Character':['Ariel','JF','Gallo','Iago','Logan'],'Iniciativa':[],'Vida':[],'Succes':[],'Failure':[]}
    for i in range(5):
        while True:
            try:
                inic = int(input(slow_print(f'Ingrese la Iniciativa de {PC["Character"][i]}',0.005)))
                break
            except ValueError:
                print(f'ERROR, Ingrese un número')
        
        PC['Iniciativa'].append(inic)
        PC['Vida'].append(df_c_data['HP'][i])
        PC['Succes'].append(0)
        PC['Failure'].append(0)
    c_data = pd.DataFrame(PC)
    inic_pool = pd.concat([inic_pool,c_data],ignore_index=True)
    inic_pool = inic_pool.sort_values('Iniciativa',ascending = False)
    inic_pool = inic_pool.reset_index(drop=True)    
    return inic_pool

#Crear NPC
def inic_call_enemy(inic_pool):  
    inic_enemigos ={'Character':[],'Iniciativa':[],'Vida':[],'Succes':[],'Failure':[]}
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
    inic_enemigos['Succes'].append(None)
    inic_enemigos['Failure'].append(None)
    c_data = pd.DataFrame(inic_enemigos)
    inic_pool = pd.concat([inic_pool,c_data],ignore_index=True)
    inic_pool = inic_pool.sort_values('Iniciativa',ascending = False)
    inic_pool = inic_pool.reset_index(drop=True)
    slow_print('Base de datos actualizada correctamente, enemigo añadido.',0.01)      
    return inic_pool

#Eliminar PC/NPC
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

#Cambiar Vida
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
    slow_print('Valores Actualizados.\n',0.02)
    print(inic_pool)
    return inic_pool

#CSV-->main
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

#Tiros de salvacion
def death_saving_throw(inic_pool, turno_name):
    while True:
        try:
            result = int(input(slow_print(f'\n{inic_pool.loc[inic_pool["Character"] == turno_name, "Character"].iloc[0]} está abatido. Ingrese el resultado del tiro de salvación del jugador', 0.01)))
            if result < 1 or result > 20:
                continue
            else:
                break
        except ValueError:
            print('ERROR, Ingrese un número')
    if result == 1:
        inic_pool.loc[inic_pool['Character'] == turno_name, 'Failure'] += 2
    elif result in range(2, 10):
        inic_pool.loc[inic_pool['Character'] == turno_name, 'Failure'] += 1
    elif result in range(10, 19):
        inic_pool.loc[inic_pool['Character'] == turno_name, 'Succes'] += 1
    elif result == 20:
        inic_pool.loc[inic_pool['Character'] == turno_name, 'Succes'] = 3
        inic_pool.loc[inic_pool['Character'] == turno_name, 'Failure'] = 0

    if inic_pool.loc[inic_pool['Character'] == turno_name, 'Succes'].iloc[0] == 3:
        slow_print('\nEl Personaje logró todos los tiros de salvación.\n', 0.01)
        inic_pool.loc[inic_pool['Character'] == turno_name, 'Succes'] = 0
        inic_pool.loc[inic_pool['Character'] == turno_name, 'Failure'] = 0
        inic_pool.loc[inic_pool['Character'] == turno_name, 'Vida'] = '1'
    elif inic_pool.loc[inic_pool['Character'] == turno_name, 'Failure'].iloc[0] >= 3:
        slow_print('\nEl Personaje muere.\n', 0.01)
    else:
        slow_print(f'\nEl Personaje tiene {inic_pool.loc[inic_pool["Character"] == turno_name, "Succes"].iloc[0]} tiradas logradas y {inic_pool.loc[inic_pool["Character"] == turno_name, "Failure"].iloc[0]} tiradas falladas\n', 0.01)
    return inic_pool

#csv --> Data
def csv_read():
    file = open('resources\\pool.csv','r')
    data = file.readlines()
    file.close
    data = list(map(tablenator,data))
    pool = {'Character':[],'Iniciativa':[],'Vida':[],'Succes':[],'Failure':[]}
    data.pop(0)
    for lista in data:
        for item in range(len(lista)):
            key = list(pool.keys())[item]
            pool[key].append(lista[item])
    df_pool = pd.DataFrame(pool)
    return df_pool