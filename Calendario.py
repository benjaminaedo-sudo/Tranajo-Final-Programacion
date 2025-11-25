import tkinter as tk # Importa la librería tkinter para la interfaz gráfica
from tkinter import ttk # Importa ttk para widgets avanzados (Combobox)
from calendar import monthcalendar # No se usa en el código final, pero estaba importado
from datetime import date # Importa date para obtener el año actual

def mostrar():
    """Genera y muestra la lista de días de Trabajo/Descanso según los parámetros."""
    # Borra el contenido actual del Text widget
    txt.delete(1.0, tk.END) 
    
    # Obtiene y convierte los valores de entrada a enteros
    mes, año = int(cmb_mes.get()), int(ent_año.get()) 
    ini, fin = int(ent_ini.get()), int(ent_fin.get()) 
    
    # Obtiene el patrón de turno (ej. "4x4") y lo divide en días de trabajo (trab) y descanso (desc)
    trab, desc = map(int, cmb_mod.get().split('x')) 
    ciclo = trab + desc # Calcula la duración total del ciclo (ej. 4+4=8)
    
    c = 0 # Contador para rastrear el día dentro del ciclo
    
    # Itera sobre el rango de días especificado (desde 'ini' hasta 'fin' inclusive)
    for d in range(ini, fin + 1):
        # Determina el estado: si el resto de c/ciclo es menor que 'trab', es Trabajo
        estado = "Trabajo" if c % ciclo < trab else "Descanso"
        # Inserta la línea formateada en el Text widget
        txt.insert(tk.END, f"{d:2d}-{mes}-{año}: {estado}\n") 
        c += 1 # Incrementa el contador del ciclo

# --- Configuración de la Ventana Principal ---
v = tk.Tk(); v.title("Planificador de Turnos")

# --- Widgets de Interfaz (Etiquetas y Entradas) ---

# Mes (Label y Combobox)
tk.Label(v, text="Mes").grid(row=0, column=0)
cmb_mes=ttk.Combobox(v,values=list(range(1,13)),width=4)
cmb_mes.grid(row=0,column=1)

# Año (Label y Entry con valor inicial del año actual)
tk.Label(v, text="Año").grid(row=0,column=2)
ent_año=tk.Entry(v,width=5)
ent_año.insert(0,date.today().year)
ent_año.grid(row=0,column=3)

# Día de Inicio (Label y Entry con valor inicial '1')
tk.Label(v, text="Inicio").grid(row=1,column=0)
ent_ini=tk.Entry(v,width=4)
ent_ini.insert(0,1)
ent_ini.grid(row=1,column=1)

# Día de Término (Label y Entry con valor inicial '30')
tk.Label(v, text="Término").grid(row=1,column=2)
ent_fin=tk.Entry(v,width=4)
ent_fin.insert(0,30)
ent_fin.grid(row=1,column=3)

# Patrón de Turno (Label y Combobox con opciones predefinidas)
tk.Label(v, text="Turno").grid(row=1,column=4)
cmb_mod=ttk.Combobox(v,values=["4x4","7x7","14x14"],width=6)
cmb_mod.grid(row=1,column=5)

# Botón 'Mostrar': llama a la función 'mostrar'
tk.Button(v,text="Mostrar",command=mostrar).grid(row=1,column=6)

# Área de Texto (Text) para mostrar los resultados
txt=tk.Text(v,width=38,height=15)
# Se posiciona en la fila 2 y se expande por 7 columnas
txt.grid(row=2,column=0,columnspan=7) 

v.mainloop() # Inicia el bucle principal de la aplicación GUI