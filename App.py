import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

# Configuración del estilo de la página
def configurar_estilo():
    st.set_page_config(
        page_title="CRECR - El retiro es primero",
        page_icon="🤑",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        """
        <style>
        body {
            background-color: #EFEEE7;
        }
        .stButton>button {
            color: white;
            background-color: #2596be;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

configurar_estilo()

# Formulario de información
def formulario_informacion():
    st.header("Formulario de Inversión en Siefore")
    monto_aportacion = st.number_input("¿De cuánto serán tus aportaciones mensuales?", min_value=0, step=100, format="%d")
    enfoque_inversion = st.selectbox("¿Tienes un enfoque a corto, mediano o largo plazo?", ["Corto plazo (1-3 años)", "Mediano plazo (4-7 años)", "Largo plazo (8+ años)"])
    gusta_tequila = st.selectbox("¿Te gusta el tequila?", ["Sí", "No"])
    return monto_aportacion, enfoque_inversion, gusta_tequila

# Obtener datos de Yahoo Finance
def obtener_datos_yfinance(symbols, start_date, end_date):
    data = yf.download(symbols, start=start_date, end=end_date)["Adj Close"].dropna()
    return data

# Mostrar los rendimientos
def mostrar_inversiones(df_yfinance):
    st.header("Visualización de Inversiones")
    st.write(df_yfinance)
    fig = px.line(df_yfinance, x=df_yfinance.index, y=df_yfinance.columns, title="Rendimientos Históricos del portafolio de CRECR")
    st.plotly_chart(fig, use_container_width=True)

informacion_usuario = formulario_informacion()

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    if st.button("¡Cómo se ve mi inversión?", help="Haz clic para ver tu inversión", key="enviar_informacion"):
        st.success(f"¡Información enviada! Tus respuestas fueron: Aportaciones de ${informacion_usuario[0]} mensuales, enfoque a {informacion_usuario[1]}, y {'sí te gusta' if informacion_usuario[2] == 'Sí' else 'no te gusta'} el tequila.")
        symbols = ["AC.MX", "GCARSOA1.MX", "GRUMAB.MX", "ALSEA.MX", "GAPB.MX", "ASURB.MX", "DIA", "SPY"]
        start_date = "2014-05-01"
        end_date = "2024-04-28"
        df_yfinance = obtener_datos_yfinance(symbols, start_date, end_date)
        mostrar_inversiones(df_yfinance)
