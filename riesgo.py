import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Simular datos y entrenar el modelo (igual que antes)
np.random.seed(123)
n = 300
data = pd.DataFrame({
    'faltas': np.random.poisson(3, n),
    'promedio': np.round(np.random.uniform(5, 10, n), 2),
    'horas_estudio': np.random.randint(0, 15, n),
    'participacion': np.random.randint(1, 6, n),
    'dificultad_percibida': np.random.randint(1, 6, n)
})

# Crear variable objetivo
data['riesgo'] = (
    (data['faltas'] > 5) |
    (data['promedio'] < 6) |
    (data['horas_estudio'] < 3) |
    ((data['participacion'] <= 2) & (data['dificultad_percibida'] >= 4))
).astype(int)

# Entrenar modelo
X = data[['faltas', 'promedio', 'horas_estudio', 'participacion', 'dificultad_percibida']]
y = data['riesgo']
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Interfaz en Streamlit
st.title("📘 Riesgo de Reprobar una Materia")
st.write("Ingresa tus datos académicos para estimar tu riesgo.")

faltas = st.slider("Número de faltas", 0, 15, 3)
promedio = st.slider("Promedio actual", 5.0, 10.0, 8.0, step=0.1)
horas = st.slider("Horas de estudio por semana", 0, 20, 5)
participacion = st.slider("Participación en clase (1=ninguna, 5=muy alta)", 1, 5, 3)
dificultad = st.slider("Dificultad percibida del curso", 1, 5, 3)

# Predicción
entrada = np.array([[faltas, promedio, horas, participacion, dificultad]])
prob = model.predict_proba(entrada)[0][1]
riesgo = model.predict(entrada)[0]

st.subheader("Resultado")

st.write(f"🔎 **Probabilidad estimada de reprobar:** {prob*100:.1f}%")

if riesgo == 1:
    st.error("⚠️ Estás en riesgo alto de reprobar. Recomendaciones:")
    if promedio < 6.5:
        st.write("- 📉 Mejora tu promedio académico.")
    if faltas > 5:
        st.write("- 📅 Reduce tus faltas.")
    if horas < 5:
        st.write("- 📚 Aumenta tus horas de estudio.")
    if participacion <= 2:
        st.write("- 🙋 Participa más en clase.")
    if dificultad >= 4:
        st.write("- 🧠 Busca apoyo con tutorías.")
else:
    st.success("✅ Bajo riesgo de reprobar. ¡Sigue así!")
