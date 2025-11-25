#Nombre: Benjamin Aedo
# Profesor: Melquisedec Sierra
# Fecha: 11-11-2025
# Descripción: Este código utiliza programación orientada a objetos para representar un país con sus regiones y graficar la población de cada región usando Matplotlib.
import matplotlib.pyplot as plt # Importa la librería Matplotlib para gráficos

# Clases para representar regiones y país
class Region:
    """Clase para representar una región con su nombre y población."""
    def __init__(self, nombre, poblacion):
        """Constructor de la clase Region."""
        self.nombre = nombre # Nombre de la región (atributo)
        self.poblacion = poblacion # Población de la región (atributo)
#Esta parte del código define una clase llamada "Region" que tiene dos atributos, lo cuales son nombre y poblacion

class Pais:
    """Clase para representar un país, que contiene una lista de objetos Region."""
    def __init__(self, nombre, regiones):
        """Constructor de la clase Pais."""
        self.nombre = nombre # Nombre del país (atributo)
        self.regiones = regiones # Lista de objetos Region (atributo)

    def graficar(self):
        """Método que genera y muestra un gráfico de barras de la población por región."""
        # Crea una lista de nombres de regiones
        nombres = [r.nombre for r in self.regiones]
        # Crea una lista de poblaciones de regiones
        poblaciones = [r.poblacion for r in self.regiones] 

        # Crea el gráfico de barras
        plt.bar(nombres, poblaciones, color=["skyblue", "lightgreen", "salmon"])
        # Establece el título del gráfico
        plt.title(f"Población por regiones de {self.nombre}")
        # Etiqueta del eje X
        plt.xlabel("Regiones")
        # Etiqueta del eje Y
        plt.ylabel("Habitantes") 

        # Mostrar números sobre las barras
        for i, p in enumerate(poblaciones):
            # Añade el texto de la población sobre cada barra, formateando el número
            plt.text(i, p + 100000, f"{p:,}", ha="center") 

        plt.show() # Muestra la ventana del gráfico

# Crear regiones y mostrar gráfico
# Instanciación de objetos Region
norte = Region("Norte", 6000000) 
centro = Region("Centro", 9000000)
sur = Region("Sur", 5000000)

# Instanciación de objeto Pais, pasando las regiones
siria = Pais("Siria", [norte, centro, sur]) 
# Llama al método graficar() del objeto Pais para generar el gráfico
siria.graficar()

# Se uso POO para crear las regiones y el país, y luego se graficó la población por regiones usando Matplotlib.