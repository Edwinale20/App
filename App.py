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
st.set_page_config(page_title="CRECR - El retiro es primero", page_icon="📶", layout="wide")

# Usar HTML y CSS para añadir un título centrado
st.markdown("""
<style>
body { background-color: #EFEEE7; }
.stButton>button { color: white; background-color: #2596be; }
</style>
""", unsafe_allow_html=True)

# Título centrado
st.markdown("<h1 style='text-align: center;'>CRECR - El retiro es primero</h1>", unsafe_allow_html=True)

# Paso 2: Crear un formulario centrado en la página principal para recoger información del usuario
st.header("🛡️ Visualización de Inversión en Siefore de CRECR")
col1, col2, col3 = st.columns([1,1,1])

with col2:  # Usar la columna central para los inputs
    monto_inversion = st.number_input("💲 Cantidad a invertir inicialmente:", min_value=0, step=1000, value=10000)
    monto_aportacion = st.number_input("📆 ¿De cuánto serán tus aportaciones mensuales?", min_value=0, step=100)
    enfoque_inversion = st.selectbox("📝 ¿Cuál es tu edad?", ["20-30 años", "31-40 años", "41-50 años", "51+ años"])


# PASO 4: Interacción con botón y visualización de la inversión
import streamlit as st
import pandas as pd
import plotly.express as px

# Definir las variables de acciones y sus pesos globalmente
acciones = ['AC.MX', 'GCARSOA1.MX', 'GRUMAB.MX', 'ALSEA.MX', 'GAPB.MX', 'ASURB.MX', 'DIA', 'SPY']
pesos = [18.41, 5.00, 5.00, 5.00, 20.00, 11.77, 14.82, 20.00]  # Porcentajes como valores decimales

# Crear columnas para distribuir la visualización de la información
col1, col2 = st.columns(2)

with col1:  # Visualizaciones gráficas en la primera columna
    if st.button('¿Cómo se ve mi inversión? 💼', key='1'):  # Asegura usar un key único si tienes múltiples botones
        # Subpaso 1: Calcular la suma de la inversión inicial y la aportación mensual
        total_inversion = monto_inversion + monto_aportacion
        st.write(f'Esta es tu aportación mensual: ${total_inversion} 💼')

        # Subpaso 2: Crear un gráfico de pie con la distribución de la inversión en acciones
        inversion_por_accion = [total_inversion * peso / 100 for peso in pesos]
        fig_pie = px.pie(names=acciones, values=inversion_por_accion, title="Distribución de la Inversión en Acciones")
        st.plotly_chart(fig_pie)

        # Subpaso 3: Gráfica de comparación de los últimos 10 años de nuestro portafolio con la TIIE
        df = pd.read_csv('comparacion.csv')  # Asegúrate de que el archivo está en el directorio correcto
        fig_line = px.line(df, x='Fecha', y=['TIIE', 'CRECR'], title='Comparación de la Inversión CRECR con TIIE 📈', labels={'value': 'Valor', 'variable': 'Índice'})
        st.plotly_chart(fig_line)

with col2:  # Listado de acciones y sus pesos en la segunda columna
    st.write("## Acciones y sus Pesos")
    for accion, peso in zip(acciones, pesos):
        st.write(f"{accion}: {peso}%")



