import tkinter as tk # Importa la librería tkinter para la interfaz gráfica

# --- Configuración Inicial de la Ventana ---
ventana = tk.Tk() # Crea la ventana principal
ventana.title("Calculadora Básica") # Establece el título de la ventana

ancho_base = 300
alto_base = 400
# Establece el tamaño inicial de la ventana
ventana.geometry(f"{ancho_base}x{alto_base}") 
# Establece el tamaño mínimo permitido para la ventana
ventana.minsize(300, 400) 

# --- Componente de Entrada (Display) ---
# Crea un campo de entrada para mostrar números y resultados
entrada = tk.Entry(ventana, width=25, borderwidth=5, font=("Arial", 16))
# Empaqueta el campo de entrada en la ventana con un margen vertical
entrada.pack(pady=10) 

# --- Contenedor de Botones ---
# Crea un frame (marco) para organizar los botones en una cuadrícula
frame_botones = tk.Frame(ventana)
frame_botones.pack(expand=True) # Empaqueta el frame, permitiéndole expandirse

# --- Funciones de la Calculadora ---

def click(num):
    """Maneja el evento de click en los botones numéricos y operadores."""
    actual = entrada.get() # Obtiene el contenido actual del display
    entrada.delete(0, tk.END) # Borra el contenido actual
    # Inserta el contenido previo más el nuevo número/operador
    entrada.insert(0, actual + str(num)) 

def limpiar():
    """Borra completamente el contenido del display."""
    entrada.delete(0, tk.END)

def calcular():
    """Evalúa la expresión en el display y muestra el resultado."""
    try:
        # Utiliza eval() para calcular el resultado de la expresión
        resultado = eval(entrada.get()) 
        entrada.delete(0, tk.END)
        entrada.insert(0, resultado) # Muestra el resultado
    except:
        # Maneja errores de sintaxis o división por cero
        entrada.delete(0, tk.END)
        entrada.insert(0, "Error")

# --- Definición y Creación de Botones ---

# Lista de tuplas: (texto_del_botón, fila, columna)
botones = [
    ('7',1,0), ('8',1,1), ('9',1,2), ('/',1,3),
    ('4',2,0), ('5',2,1), ('6',2,2), ('*',2,3),
    ('1',3,0), ('2',3,1), ('3',3,2), ('-',3,3),
    ('0',4,0), ('.',4,1), ('+',4,2), ('=',4,3)
]

# Itera sobre la lista para crear y posicionar los botones
for (texto, fila, col) in botones:
    if texto == '=':
        # Botón de igual: llama a la función calcular
        tk.Button(frame_botones, text=texto, width=5, height=2, command=calcular).grid(row=fila, column=col, padx=5, pady=5)
    else:
        # Otros botones: llaman a la función click con su propio texto
        # Se usa lambda para pasar argumentos al comando
        tk.Button(frame_botones, text=texto, width=5, height=2, command=lambda t=texto: click(t)).grid(row=fila, column=col, padx=5, pady=5)

# Botón 'C' (Limpiar): se extiende por 4 columnas (columnspan=4)
tk.Button(frame_botones, text='C', width=22, height=2, command=limpiar).grid(row=5, column=0, columnspan=4, padx=5, pady=5)

# --- Funcionalidades Adicionales (Centrar y Pantalla Completa) ---

def centrar_ventana():
    """Calcula y establece la posición de la ventana para centrarla en la pantalla."""
    ventana.update_idletasks() # Asegura que la ventana obtenga sus dimensiones reales
    ancho_pantalla = ventana.winfo_screenwidth() # Ancho de la pantalla
    alto_pantalla = ventana.winfo_screenheight() # Alto de la pantalla
    ancho_ventana = ventana.winfo_width() # Ancho de la ventana
    alto_ventana = ventana.winfo_height() # Alto de la ventana
    # Calcula la posición X e Y para centrar
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    # Establece la nueva geometría de la ventana (solo posición)
    ventana.geometry(f"+{x}+{y}") 

def toggle_fullscreen(event=None):
    """Activa o desactiva el modo de pantalla completa."""
    # Obtiene el estado actual de la pantalla completa
    fullscreen = not ventana.attributes("-fullscreen")
    # Establece el nuevo estado
    ventana.attributes("-fullscreen", fullscreen)
    # Centra la ventana después de un pequeño retraso (importante para el centrado)
    ventana.after(100, centrar_ventana)

# Asocia la tecla F11 a la función toggle_fullscreen
ventana.bind("<F11>", toggle_fullscreen)
centrar_ventana() # Llama a centrar_ventana al inicio para posicionar la ventana
ventana.mainloop() # Inicia el bucle principal de la aplicación GUI