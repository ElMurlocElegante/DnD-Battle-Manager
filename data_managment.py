import pandas as pd
import matplotlib.pyplot as plt
import re
from menus import *
from screen_config import*
def eliminar_contenido_fuera_de_parentesis(texto):
    contenido_entre_parentesis = re.findall(r'\(([^)]*)\)', texto)
    if contenido_entre_parentesis:
        return "".join(contenido_entre_parentesis)
    else:
        return ""

def eliminar_contenido_entre_parentesis(texto):
    return re.sub(r'\([^)]*\)', '', texto)

def eliminar_contenido_entre_corchetes(texto):
    return re.sub(r'\[[^\[\]]*\]', '', texto)

# file = open('resources\\Bestiary.csv','r')
# data = file.readlines()
# file.close()
# for i in range(len(data)):
#     data[i] = data[i].replace('","','";"')

# file = open('resources\\Bestiary_g.csv','w')
# file.writelines(data)
# file.close

df_monster = pd.read_csv('resources\\Bestiary_g.csv',sep=';')
df_monster['HP'] = df_monster['HP'].apply(eliminar_contenido_fuera_de_parentesis)


df_monster = df_monster.loc[df_monster['CR'] != 'Nan']
df_monster = df_monster.loc[df_monster['HP'] != 'Nan']
df_monster['HP'] = df_monster['HP'].apply(eliminar_contenido_entre_parentesis)
df_monster['CR'] = df_monster['CR'].astype(str).apply(eliminar_contenido_entre_parentesis)
df_monster['CR']= df_monster['CR'].replace(['1/8','1/4','1/2'],[0.125,0.25,0.5])

expresion_regular = r'\b(\d+)\b'
df_monster['CR'] = df_monster['CR'].str.extract(expresion_regular, expand=False)

df_monster['HP'] = df_monster['HP'].str.strip()
df_monster['CR'] = df_monster['CR'].str.strip()
# df_monster['HP'] = pd.to_numeric(df_monster['HP'])
df_monster['CR'] = pd.to_numeric(df_monster['CR'])

