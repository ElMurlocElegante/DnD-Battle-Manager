import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Funciones matemáticas
def function1(x):
    return np.sin(x)

def function2(x):
    return np.cos(x)

# Función de inicialización del gráfico
def init():
    lines[0].set_data([], [])
    lines[1].set_data([], [])
    return lines

# Función de actualización del gráfico en cada fotograma
def update(frame):
    x = np.linspace(0, 2*np.pi, 100)
    y1 = function1(x + frame*0.1)  # Actualiza la función1 en cada fotograma
    y2 = function2(x + frame*0.1)  # Actualiza la función2 en cada fotograma

    lines[0].set_data(x, y1)
    lines[1].set_data(x, y2)
    return lines

# Crear la figura y los objetos de las líneas
fig, ax = plt.subplots()
lines = [ax.plot([], [], lw=2)[0] for _ in range(2)]

# Configurar los límites del gráfico
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1, 1)

# Crear la animación
ani = FuncAnimation(fig, update, frames=100, init_func=init, blit=True)

# Mostrar la animación
plt.show()