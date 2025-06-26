import streamlit as st

# --- Preguntas y opciones ---
preguntas = [
    ("¿Qué actividad disfrutas más?", ["Leer artículos científicos", "Pintar o dibujar", "Reparar cosas", "Ayudar a personas"]),
    ("¿Qué asignatura prefieres?", ["Matemáticas", "Arte", "Tecnología", "Psicología"]),
    ("¿Cómo te gusta trabajar?", ["Analizando datos", "Creando cosas nuevas", "Con herramientas", "En equipo con personas"]),
    ("¿Qué hobby te interesa más?", ["Resolver acertijos", "Tocar un instrumento", "Armar circuitos", "Voluntariado"]),
    ("¿Qué valoras más en un trabajo?", ["Descubrimiento", "Expresión", "Precisión", "Impacto social"]),
    ("¿Con qué palabra te identificas más?", ["Lógico", "Creativo", "Práctico", "Empático"])
]

# --- Mapeo a perfiles ---
perfil_map = {
    "Leer artículos científicos": "científico",
    "Matemáticas": "científico",
    "Analizando datos": "científico",
    "Resolver acertijos": "científico",
    "Descubrimiento": "científico",
    "Lógico": "científico",
    "Pintar o dibujar": "artístico",
    "Arte": "artístico",
    "Creando cosas nuevas": "artístico",
    "Tocar un instrumento": "artístico",
    "Expresión": "artístico",
    "Creativo": "artístico",
    "Reparar cosas": "técnico",
    "Tecnología": "técnico",
    "Con herramientas": "técnico",
    "Armar circuitos": "técnico",
    "Precisión": "técnico",
    "Práctico": "técnico",
    "Ayudar a personas": "social",
    "Psicología": "social",
    "En equipo con personas": "social",
    "Voluntariado": "social",
    "Impacto social": "social",
    "Empático": "social"
}

# --- Recomendaciones ---
recomendaciones = {
    "científico": "🔬 Perfil Científico: Podrías destacar en áreas como Física, Matemáticas, Biología, Ingeniería o Investigación.",
    "artístico": "🎨 Perfil Artístico: Podrías sobresalir en Diseño, Música, Artes Visuales, Publicidad o Cine.",
    "técnico": "🔧 Perfil Técnico: Carreras como Mecatrónica, Robótica, Sistemas o Mantenimiento son una excelente opción.",
    "social": "👥 Perfil Social: Psicología, Educación, Trabajo Social o Comunicación podrían ser tu vocación."
}

# --- Estado inicial seguro ---
if "respuestas" not in st.session_state:
    st.session_state.respuestas = []

if "finalizado" not in st.session_state:
    st.session_state.finalizado = False

# --- Título y progreso ---
st.title("🧭 Test Vocacional Interactivo")
progreso = len(st.session_state.respuestas)
st.progress(progreso / len(preguntas))

# --- Lógica principal ---
if not st.session_state.finalizado:
    if progreso < len(preguntas):
        pregunta, opciones = preguntas[progreso]
        st.write(f"**{pregunta}**")
        seleccion = st.radio("Selecciona una opción:", opciones, key=f"preg_{progreso}")

        if st.button("Siguiente"):
            st.session_state.respuestas.append(seleccion)

    if len(st.session_state.respuestas) == len(preguntas):
        st.session_state.finalizado = True

# --- Mostrar resultado ---
if st.session_state.finalizado:
    conteo = {"científico": 0, "artístico": 0, "técnico": 0, "social": 0}
    for r in st.session_state.respuestas:
        perfil = perfil_map.get(r)
        if perfil:
            conteo[perfil] += 1
    perfil_final = max(conteo, key=conteo.get)

    st.success("✅ Test completado.")
    st.markdown(f"### 🔎 Tu perfil vocacional dominante es: **{perfil_final.upper()}**")
    st.info(recomendaciones[perfil_final])

    st.subheader("📋 Respuestas seleccionadas:")
    for i, r in enumerate(st.session_state.respuestas):
        st.write(f"{i+1}. {preguntas[i][0]} → {r}")

    if st.button("🔄 Reiniciar"):
        st.session_state.respuestas = []
        st.session_state.finalizado = False