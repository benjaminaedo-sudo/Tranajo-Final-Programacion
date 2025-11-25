import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ==========================================
# 1. CONFIGURACIÓN Y DATOS
# ==========================================

# Parámetros del Algoritmo Genético
TAMAÑO_POBLACION = 20    # Cuántas "recetas" probamos por generación
GENERACIONES = 15        # Cuántas veces evolucionamos
PROB_MUTACION = 0.2      # Probabilidad de cambiar un ingrediente al azar
ELITISMO = 2             # Cuántos de los mejores pasan directo a la sig. generación

# Definición del "ADN" (Rangos de los Hiperparámetros)
# Gen 0: n_estimators (Cantidad de árboles) -> entre 10 y 200
# Gen 1: max_depth (Profundidad del árbol)  -> entre 1 y 30
# Gen 2: min_samples_split (Mínimo para dividir) -> entre 2 y 20
RANGOS = [(10, 200), (1, 30), (2, 20)]

# Cargar el dataset (Vinos)
data = load_wine()
X, y = data.data, data.target
# Separamos datos para entrenar (train) y para evaluar (test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ==========================================
# 2. FUNCIONES DEL ALGORITMO GENÉTICO
# ==========================================

def crear_individuo():
    """Crea una configuración aleatoria (un individuo)."""
    return [random.randint(r[0], r[1]) for r in RANGOS]

def crear_poblacion(tamano):
    """Crea la población inicial."""
    return [crear_individuo() for _ in range(tamano)]

def fitness(individuo):
    """
    Función de Aptitud:
    1. Toma los genes del individuo.
    2. Configura el modelo de Scikit-Learn.
    3. Retorna la precisión (accuracy).
    """
    n_est, depth, min_split = individuo
    
    # Aquí ocurre la magia: Usamos los genes para configurar el modelo
    clf = RandomForestClassifier(
        n_estimators=n_est,
        max_depth=depth,
        min_samples_split=min_split,
        random_state=42,
        n_jobs=-1 # Usar todos los núcleos del procesador
    )
    
    clf.fit(X_train, y_train)
    predictions = clf.predict(X_test)
    
    return accuracy_score(y_test, predictions)

def seleccion_torneo(poblacion, scores, k=3):
    """Selecciona un padre mediante un torneo entre k individuos."""
    seleccionados = random.sample(list(zip(poblacion, scores)), k)
    # Retorna el individuo con el mejor score del grupo seleccionado
    return max(seleccionados, key=lambda x: x[1])[0]

def cruce(padre1, padre2):
    """Cruce de un punto: mezcla la mitad de los genes de cada padre."""
    punto = random.randint(1, len(padre1)-1)
    hijo = padre1[:punto] + padre2[punto:]
    return hijo

def mutacion(individuo):
    """Con baja probabilidad, cambia un gen al azar."""
    if random.random() < PROB_MUTACION:
        gen_idx = random.randint(0, len(individuo)-1)
        rango = RANGOS[gen_idx]
        individuo[gen_idx] = random.randint(rango[0], rango[1])
    return individuo

# ==========================================
# 3. EJECUCIÓN DEL ALGORITMO (MAIN LOOP)
# ==========================================

poblacion = crear_poblacion(TAMAÑO_POBLACION)
historial_scores = [] # Para graficar después

# --- CORRECCIÓN AQUÍ: Usamos len() en lugar de .shape[0] ---
print(f"--- Iniciando optimización para {len(data.feature_names)} características ---")

for gen in range(GENERACIONES):
    # 1. Evaluar Fitness
    scores = [fitness(ind) for ind in poblacion]
    
    # Guardar estadísticas
    mejor_score = max(scores)
    mejor_ind = poblacion[np.argmax(scores)]
    historial_scores.append(mejor_score)
    
    print(f"Gen {gen+1}: Mejor Accuracy = {mejor_score:.4f} | Config: {mejor_ind}")
    
    # 2. Elitismo (Los mejores pasan intactos)
    # Ordenamos población por score descendente
    ordenados = sorted(zip(poblacion, scores), key=lambda x: x[1], reverse=True)
    nueva_poblacion = [ind for ind, score in ordenados[:ELITISMO]]
    
    # 3. Generar el resto de la nueva población
    while len(nueva_poblacion) < TAMAÑO_POBLACION:
        p1 = seleccion_torneo(poblacion, scores)
        p2 = seleccion_torneo(poblacion, scores)
        hijo = cruce(p1, p2)
        hijo = mutacion(hijo)
        nueva_poblacion.append(hijo)
        
    poblacion = nueva_poblacion

# ==========================================
# 4. RESULTADOS FINALES
# ==========================================

print("\n" + "="*40)
print("MEJOR CONFIGURACIÓN ENCONTRADA")
print("="*40)
print(f"Precisión Final: {max(historial_scores):.4f}")
print(f"Árboles (n_estimators): {mejor_ind[0]}")
print(f"Profundidad (max_depth): {mejor_ind[1]}")
print(f"División Mínima (min_samples): {mejor_ind[2]}")

# Gráfico de evolución
plt.figure(figsize=(10, 5))
plt.plot(historial_scores, marker='o', linestyle='-', color='b')
plt.title('Evolución de la Precisión del Modelo')
plt.xlabel('Generación')
plt.ylabel('Precisión (Accuracy)')
plt.grid(True)
plt.show()