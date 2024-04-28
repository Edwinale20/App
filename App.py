import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

def cuestionario_perfil_riesgo():
    st.header("Cuestionario de Perfil de Riesgo")

    preguntas = {
        "¿Cuál es su edad?": ["Menos de 30", "30-45", "45-60", "Más de 60"],
        "¿Cuál es su nivel de experiencia en inversión?": ["Ninguna", "Poca", "Moderada", "Alta"],
        "¿Cuál es su tolerancia al riesgo?": ["Baja", "Moderada", "Alta"],
        "¿Cuál es su horizonte de inversión?": ["Corto plazo (1-3 años)", "Mediano plazo (4-7 años)", "Largo plazo (8+ años)"],
        "¿Cuál es su objetivo de inversión?": ["Conservador", "Moderado", "Agresivo"]
    }

    respuestas = {}

    for pregunta, opciones in preguntas.items():
        respuesta = st.selectbox(pregunta, opciones)
        respuestas[pregunta] = respuesta

    return respuestas

# Configuración del estilo de la aplicación con emojis
def configurar_estilo():
    # Establecer el color de fondo
    st.markdown(
        """
        <style>
        body {
            background-color: #EFEEE7;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Establecer emojis para el título de la página
    st.set_page_config(
        page_title="CRECR - Ayuda a crecer tus inversiones", 
        page_icon="💹", 
        layout="wide"
    )

# Configurar el estilo de la aplicación con emojis
configurar_estilo()

# Mostrar el cuestionario al iniciar la aplicación
respuestas_cuestionario = cuestionario_perfil_riesgo()

# Resto del código de la aplicación...

