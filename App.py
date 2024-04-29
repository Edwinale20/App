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
st.markdown("""
<style>
body { background-color: #EFEEE7; }
.stButton>button { color: white; background-color: #2596be; }
h1 { text-align: center; }
</style>
<h1>CRECR - El retiro es primero</h1>
""", unsafe_allow_html=True)

# Paso 2: Crear un formulario centrado en la página principal para recoger información del usuario
st.header("🛡️ Visualización de Inversión en Siefore de CRECR")
col1, col2, col3 = st.columns([1,1,1])

with col2:  # Usar la columna central para los inputs
    monto_inversion = st.number_input("💲 Cantidad a invertir inicialmente:", min_value=0, step=1000, value=10000)
    monto_aportacion = st.number_input("📆 ¿De cuánto serán tus aportaciones mensuales?", min_value=0, step=100)
    enfoque_inversion = st.selectbox("📝 ¿Cuál es tu edad?", ["20-30 años", "31-40 años", "41-50 años", "51+ años"])


# PASO 3: Interacción con botón y visualización de la inversión

# Definir las variables de acciones y sus pesos globalmente
acciones = ['AC.MX', 'GCARSOA1.MX', 'GRUMAB.MX', 'ALSEA.MX', 'GAPB.MX', 'ASURB.MX', 'DIA', 'SPY']
pesos = [18.41, 5.00, 5.00, 5.00, 20.00, 11.77, 14.82, 20.00]  # Porcentajes como valores decimales

# Inicializar session_state variables si no existen
if 'monto_inversion' not in st.session_state:
    st.session_state.monto_inversion = 10000
if 'monto_aportacion' not in st.session_state:
    st.session_state.monto_aportacion = 0

# PASO 3 y 4: Interacción con botón y visualización de la inversión
col1, col2 = st.columns(2)

with col1:  # Columna para visualizaciones gráficas
    if st.button('¿Cómo se ve mi inversión? 💼', key='1'):
        # Subpaso 1: Calcular la suma de la inversión inicial y la aportación mensual
        total_inversion = st.session_state.monto_inversion + st.session_state.monto_aportacion
        st.write(f'Esta es tu aportación mensual: ${total_inversion} 💼')

        # Subpaso 2: Crear un gráfico de pie con la distribución de la inversión en acciones
        inversion_por_accion = [total_inversion * peso / 100 for peso in pesos]
        fig_pie = px.pie(names=acciones, values=inversion_por_accion, title="Distribución de la Inversión en Acciones")
        st.plotly_chart(fig_pie)

        # Subpaso 3: Gráfica de comparación de los últimos 10 años de nuestro portafolio con la TIIE
        df = pd.read_csv('comparacion.csv')
        fig_line = px.line(df, x='Fecha', y=['Inflacion', 'CRECR'], title='Comparación de la Inversión CRECR con la tasa de inflacion 📈', labels={'value': 'Valor', 'variable': 'Índice'})
        st.plotly_chart(fig_line)

        # Subpaso 5: Proyección de Rendimientos Futuros
        data = yf.download("SPY", start="2010-01-01", end="2020-12-31")
        returns = data['Adj Close'].pct_change().dropna()
        future_years = 10
        simulations = 1000
        results = np.random.normal(returns.mean(), returns.std(), (future_years * 252, simulations))
        mean_simulation = np.mean(results, axis=1)
        cumulative_returns = np.cumprod(1 + mean_simulation) - 1
        fig_future = px.line(y=cumulative_returns, x=np.arange(2021, 2031), title='Proyección de Rendimientos Futuros del S&P 500')
        st.plotly_chart(fig_future)

with col2:  # Columna para la tabla de acciones y pesos
    if st.button('Mostrar Pesos de Acciones 💼', key='2'):
        st.write("## Acciones y sus Pesos 📊")
        data = {'Acciones': acciones, 'Pesos (%)': pesos}
        df_acciones = pd.DataFrame(data)
        st.table(df_acciones)

       # Subpaso 6: Comparación Interactiva de Portafolios con la Inflación
peso_CRECR = st.slider('Peso en CRECR', 0.0, 1.0, 0.5, 0.01)
peso_inflacion = 1 - peso_CRECR  # El resto se invierte en Inflación

# Calcular rendimientos ajustados
df['Adjusted Returns'] = df['CRECR'] * peso_CRECR + df['Inflacion'] * peso_inflacion
df['Cumulative Returns'] = (1 + df['Adjusted Returns']).cumprod() - 1

# Crear el gráfico de los rendimientos ajustados
fig_portfolio = go.Figure()
fig_portfolio.add_trace(go.Scatter(x=df.index, y=df['Cumulative Returns'], mode='lines', name='Rendimiento Cumulativo'))
fig_portfolio.update_layout(
    title='Rendimiento del Portafolio Ajustado Comparado con la Inflación',
    xaxis_title='Fecha',
    yaxis_title='Rendimiento Acumulado (%)',
    template='plotly_dark'
)
st.plotly_chart(fig_portfolio)

