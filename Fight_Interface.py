import tkinter as tk

window = tk.Tk()
window.geometry('900x720')

photo = tk.PhotoImage(file='resources\\dnd_background.png')
label = tk.Label(window,image=photo)
label.pack()
window.mainloop()