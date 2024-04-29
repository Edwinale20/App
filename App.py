# Importar las librerías necesarias
import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.express as px
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier
import plotly.graph_objects as go

# Paso 1: Configurar la página y los estilos de Streamlit
st.set_page_config(page_title="CRCER - El retiro es primero", page_icon="📶", layout="wide")

# Cargar y mostrar el logo de CRCER
logo_path = "crcer.png"  # Asegúrate de que este archivo esté en la misma carpeta que tu script de Streamlit o especifica la ruta correcta
st.image(logo_path, width=200)  # Ajusta el ancho a 200 píxeles

# Personalización de estilos y título
st.markdown("""
<style>
body { background-color: #EFEEE7; }
.stButton>button { color: white; background-color: #2596be; }
h1 { text-align: center; }
</style>
<h1>CRCER - El retiro es primero</h1>
""", unsafe_allow_html=True)


# Paso 2: Crear un formulario centrado en la página principal para recoger información del usuario
st.header("🛡️ Visualización de Inversión en Siefore de CRCER")
col1, col2, col3 = st.columns([1,1,1])

with col2:  # Usar la columna central para los inputs
    monto_inversion = st.number_input("💲 Cantidad a invertir inicialmente:", min_value=0, step=1000)
    monto_aportacion = st.number_input("📆 ¿De cuánto serán tus aportaciones mensuales?", min_value=0, step=100)
    enfoque_inversion = st.selectbox("📝 ¿Cuál es tu edad?", ["20-30 años", "31-40 años", "41-50 años", "51+ años"])


# PASO 3: Interacción con botón y visualización de la inversión

# Definir las variables de acciones y sus pesos globalmente
acciones = ['AC.MX', 'GCARSOA1.MX', 'GRUMAB.MX', 'ALSEA.MX', 'GAPB.MX', 'ASURB.MX', 'DIA', 'SPY']
pesos = [18.41, 5.00, 5.00, 5.00, 20.00, 11.77, 14.82, 20.00]  # Porcentajes como valores decimales

# Inicializar variables de session_state si no existen
if 'monto_inversion' not in st.session_state:
    st.session_state.monto_inversion = 10000
if 'monto_aportacion' not in st.session_state:
    st.session_state.monto_aportacion = 0

# PASO 4: Interacción con botón y visualización de la inversión
# Columna para visualizaciones gráficas y tabla de acciones
col1, col2 = st.columns(2)

if st.button('Visualizar Mi Inversión 💼'):
    with col1:
        # Subpaso 1: Calcular la suma de la inversión inicial y la aportación mensual
        total_inversion = st.session_state.monto_inversion + st.session_state.monto_aportacion
        st.write(f'Esta es tu aportación mensual: ${total_inversion} 💼')

        # Subpaso 2: Crear un gráfico de pie con la distribución de la inversión en acciones
        inversion_por_accion = [total_inversion * peso / 100 for peso in pesos]
        fig_pie = px.pie(names=acciones, values=inversion_por_accion)
        st.write("## Distribución de la Inversión en Acciones 🔢")
        st.plotly_chart(fig_pie)

        # Subpaso 3: Gráfica de comparación de los últimos 10 años de nuestro portafolio con la inflación
        df = pd.read_csv('comparacion.csv')
        fig_line = px.line(df, x='Fecha', y=['Inflacion', 'CRCER'], labels={'value': 'Valor', 'variable': 'Índice'})
        st.write("## Comparación de la Inversión CRCER con la tasa de inflación 💹")
        st.plotly_chart(fig_line)

    with col2:
        st.write("## Acciones y sus Pesos 📊")
        df_acciones = pd.DataFrame({'Acciones': acciones, 'Pesos (%)': pesos})
        st.table(df_acciones)

        # Subpaso 4: Proyección de crecimiento de las aportaciones mensuales
        aportacion_mensual = st.session_state.monto_aportacion
        rendimiento_mensual = 1.0123  # 1.23% de rendimiento mensual
        meses = 60 * 12  # 60 años
        saldo = [aportacion_mensual]
        for i in range(1, meses):
            saldo.append(saldo[-1] * rendimiento_mensual + aportacion_mensual)

        fig_crecimiento = go.Figure()
        fig_crecimiento.add_trace(go.Scatter(x=list(range(meses)), y=saldo, mode='lines', name='Crecimiento de Inversión'))
        fig_crecimiento.update_layout(xaxis_title='Meses', yaxis_title='Monto Acumulado ($)', template='plotly_dark')
        st.write("## Proyección de Crecimiento de la Inversión con Aportaciones Mensuales 📥")
        st.plotly_chart(fig_crecimiento)
