import pandas as pd
import streamlit as st
import yfinance as yf
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier
import plotly.graph_objects as go

# Configuración inicial de la página
def configurar_estilo():
    st.set_page_config(page_title="CRECR - El retiro es primero", page_icon="🤑", layout="wide")
    st.markdown("""
        <style>
        body { background-color: #EFEEE7; }
        .stButton>button { color: white; background-color: #2596be; }
        </style>
        """, unsafe_allow_html=True)

# Formulario para recopilar información del usuario
def formulario_informacion():
    st.header("Formulario de Inversión en Siefore")
    monto_aportacion = st.number_input("¿De cuánto serán tus aportaciones mensuales?", min_value=0, step=100)
    enfoque_inversion = st.selectbox("Elige tu enfoque de inversión", ["Corto plazo (1-3 años)", "Mediano plazo (4-7 años)", "Largo plazo (8+ años)"])
    gusta_tequila = st.selectbox("¿Te gusta el tequila?", ["Sí", "No"])
    return monto_aportacion, enfoque_inversion, gusta_tequila

# Obtención de datos financieros de Yahoo Finance
def obtener_datos_yfinance(simbolos, fecha_inicio, fecha_fin):
    return yf.download(simbolos, start=fecha_inicio, end=fecha_fin)["Adj Close"].dropna()

# Calcula los retornos diarios de las acciones
def calcular_retornos_diarios(datos):
    return datos.pct_change().dropna()

# Realiza la optimización del portafolio
def optimizar_portafolio(precios):
    mu = mean_historical_return(precios)
    S = CovarianceShrinkage(precios).ledoit_wolf()
    ef = EfficientFrontier(mu, S)
    fig = go.Figure()

    # Intenta optimizar el portafolio para una volatilidad dada
    try:
        ratios_sharpe = ef.efficient_risk(target_volatility=0.1)
        fig.add_trace(go.Scatter(x=list(ratios_sharpe.keys()), y=list(ratios_sharpe.values()), mode='lines+markers'))
        st.plotly_chart(fig, title="Frontera Eficiente")
    except ValueError:
        st.error("La volatilidad mínima alcanzable es superior a 0.1. Se mostrarán los pesos para la volatilidad mínima.")
        ef.min_volatility()
        pesos = ef.clean_weights()
        st.plotly_chart(go.Figure(data=[go.Bar(x=list(pesos.keys()), y=list(pesos.values()))]), title="Pesos del Portafolio Mínima Volatilidad")

# Configuración y ejecución de Streamlit
configurar_estilo()
usuario_info = formulario_informacion()
simbolos = ["AC.MX", "GCARSOA1.MX", "GRUMAB.MX", "ALSEA.MX", "GAPB.MX", "ASURB.MX", "DIA", "SPY"]

if st.button("Optimizar Portafolio"):
    datos = obtener_datos_yfinance(simbolos, "2014-05-01", "2024-04-28")
    optimizar_portafolio(datos)
    retornos_diarios = calcular_retornos_diarios(datos)
    st.plotly_chart(go.Figure(data=[go.Bar(x=retornos_diarios.columns, y=retornos_diarios.mean()*100)]), title="Retornos Diarios (%)")

# Gráfica de Rendimientos comparados con el TIIE
st.header("Rendimientos vs. TIIE")
tiie_data = pd.read_csv("TIIE.csv")  # Cargar datos del archivo CSV
# Añadir gráfico de línea para comparar rendimientos
tiie_fig = go.Figure()
tiie_fig.add_trace(go.Scatter(x=tiie_data["Fecha"], y=tiie_data["Rendimiento"], mode='lines', name='Rendimiento TIIE'))
tiie_fig.update_layout(title="Rendimientos vs. TIIE", xaxis_title="Fecha", yaxis_title="Rendimiento (%)")
st.plotly_chart(tiie_fig)

# Gráfica de Rendimientos Diarios de las Acciones
st.header("Rendimientos Diarios de las Acciones")
# Calcular y añadir gráfico de barras para los rendimientos diarios de las acciones
retornos_acciones_fig = go.Figure(data=[go.Bar(x=retornos_diarios.index, y=retornos_diarios[col]*100, name=col) for col in retornos_diarios.columns])
retornos_acciones_fig.update_layout(title="Rendimientos Diarios de las Acciones", xaxis_title="Fecha", yaxis_title="Rendimiento (%)")
st.plotly_chart(retornos_acciones_fig)
