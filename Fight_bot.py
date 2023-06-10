from functions import *



slow_print('-'*35,0.01)
slow_print('Bienvenido al Contador de Iniciativa',0.03)
slow_print('-'*35,0.01)

inic_pool = pd.DataFrame(columns=['Character','Iniciativa','Vida'])
character_data_structure, death_saving = read_pc_data()

slow_print('\nPor favor, ingrese las tiradas del jugador citado:\n',0.03)
inic_pool = inic_call_char(inic_pool,character_data_structure)
death_saving = death_saving_sort(death_saving,inic_pool)
print(death_saving)
while True:
    result = input(slow_print('\n----------------Menu----------------\n(1)Añadir un enemigo\n(2)Eliminar un enemigo o jugador\n(3)Reducir HP de un enemigo o jugador\n(4)Mostrar Pool actual\n(5)Iniciar Combate\n',0.01))
    if result == '1':
        inic_pool = inic_call_enemy(inic_pool)
    elif result == '2':
        inic_pool = inic_call_delete(inic_pool)
    elif result == '3':
        inic_pool = hp_modifier(inic_pool)
    elif result == '4':
        print(f'{inic_pool}\n\n{character_data_structure}')
    elif result == '5':
        break
ronda = 0
while True:
    slow_print(f'{"-"*35}Ronda N°{ronda}{"-"*35}\n',0.01)
    inic_pool_temp = inic_pool
    for turno in range(len(inic_pool['Character'])):
        turno_name = inic_pool_temp['Character'][turno]
        slow_print(f'{"-"*35}Turno de {turno_name}{"-"*35}\nVida: {inic_pool_temp["Vida"][turno]}\nIniciativa: {inic_pool_temp["Iniciativa"][turno]}\n',0.01)
        while True:
            if int(inic_pool.loc[inic_pool['Character'] == turno_name, 'Vida'].iloc[0]) <= 0:
                if turno_name in ['Ariel','JF','Gallo','Iago','Logan']:
                    if int(death_saving.loc[inic_pool['Character'] == turno_name,'Failure'].iloc[0]) >= 3:
                        slow_print('El Personaje está muerto',0.01)
                    else:
                        death_saving,inic_pool = death_saving_throw(death_saving,inic_pool,turno_name)
                break
            action = input(slow_print('Seleccione una acción de la lista.\n(1)Atacar/Curar\n(2)Mostrar Pool\n(3)Agregar NPC\n(4)Terminar Turno',0.01))
            if action == '1':
                inic_pool = hp_modifier(inic_pool)
            elif action == '2':
                print(f'{inic_pool}\n\n{character_data_structure}')
            elif action == '3':
                inic_pool = inic_call_enemy(inic_pool)
            elif action == '4':
                break
    ronda += 1
