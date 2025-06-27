
# Paso 1: Importar bibliotecas necesarias
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from ipywidgets import interact, IntSlider, FloatSlider, Output
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns

# Paso 2: Generación de datos sintéticos

np.random.seed(2025)
n = 500  # número de estudiantes simulados
data = pd.DataFrame({
    'faltas': np.random.poisson(3, n),
    'promedio': np.round(np.random.uniform(5, 10, n), 2),
    'horas_estudio': np.random.randint(0, 15, n),
    'participacion': np.random.randint(1, 6, n),  # escala 1-5
    'dificultad_percibida': np.random.randint(1, 6, n)
})

data.head()

# Paso 3: Generar la variable objetivo (1 = en riesgo de reprobar, 0 = no)

data['riesgo'] = (
    (data['faltas'] > 5) |
    (data['promedio'] < 6) |
    (data['horas_estudio'] < 3) |
    ((data['participacion'] <= 2) & (data['dificultad_percibida'] >= 4))
).astype(int)


# Paso 4: Preparar datos para el modelo

X = data[['faltas', 'promedio', 'horas_estudio', 'participacion', 'dificultad_percibida']]
y = data['riesgo']

# Separamos en conjunto de entrenamiento (80%) y de prueba (20%)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)


# Paso 5: Entrenar modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Paso 6: Predicción del modelo
y_pred = model.predict(X_test)
y_pred


# Paso 8: Interfaz interactiva con sliders
out = Output()

def predecir_riesgo(faltas, promedio, horas_estudio, participacion, dificultad_percibida):
    entrada = np.array([[faltas, promedio, horas_estudio, participacion, dificultad_percibida]])
    prob = model.predict_proba(entrada)[0][1]
    riesgo = model.predict(entrada)[0]
    with out:
        out.clear_output()
        print(f"\n🔎 Probabilidad estimada de reprobar: {prob*100:.1f}%")
        if riesgo == 1:
            print("⚠️ Riesgo alto de reprobar. Recomendaciones:")
            if promedio < 6.5: print("  - 📉 Mejora tu promedio académico.")
            if faltas > 5: print("  - 📅 Reduce tus faltas.")
            if horas_estudio < 5: print("  - 📚 Aumenta tus horas de estudio.")
            if participacion <= 2: print("  - 🙋 Participa más en clase.")
            if dificultad_percibida >= 4: print("  - 🧠 Busca apoyo con tutorías.")
        else:
            print("✅ Bajo riesgo de reprobar. ¡Sigue así!")

# Crear sliders para la interfaz
slider_faltas = IntSlider(min=0, max=15, value=3, description='Faltas')
slider_promedio = FloatSlider(min=5, max=10, step=0.1, value=8.0, description='Promedio')
slider_horas = IntSlider(min=0, max=20, value=5, description='Horas Estudio')
slider_participacion = IntSlider(min=1, max=5, value=3, description='Participación')
slider_dificultad = IntSlider(min=1, max=5, value=3, description='Dificultad')

# Mostrar la interfaz interactiva
interact(predecir_riesgo,
         faltas=slider_faltas,
         promedio=slider_promedio,
         horas_estudio=slider_horas,
         participacion=slider_participacion,
         dificultad_percibida=slider_dificultad)
display(out)
