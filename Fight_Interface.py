# import tkinter as tk

# def update_label():
    
#     label_character.config(text=(inic_pool.loc[:,['Character']]))
#     label_iniciativa.config(text=(inic_pool.loc[:,['Iniciativa']].to_string(index=False)))
#     label_vida.config(text=(inic_pool.loc[:,['Vida']]).to_string(index=False))
#     window.update()
    
#     window.after(1000, update_label)
# window = tk.Tk()
# window.title("DataFrame")
# window.geometry('900x700')
# label_character = tk.Label(window, text="", font=("Arial", 36),fg='white')
# label_iniciativa = tk.Label(window, text="", font=("Arial", 36),fg='white')
# label_vida = tk.Label(window, text="", font=("Arial", 36),fg='white', background='black',compound='bottom')
# label_character.place(x=40,y=100)
# label_iniciativa.place(x=300,y=100)
# label_vida.place(x=560,y=100)
import time
from functions import csv_read
while True:
    print(csv_read())
    time.sleep(5)
    