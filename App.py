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
st.set_page_config(page_title="📶 CRCER - Rendimiento con poco riesgo", page_icon="📶", layout="wide")

# Mostrar el logo de CRCER centrado
st.markdown("""
<div style="text-align: center;">
</div>
""", unsafe_allow_html=True)

# Personalización de estilos y título
st.markdown("""
<style>
body { background-color: #EFEEE7; }
.stButton>button { color: white; background-color: #2596be; }
h1 { text-align: center; }
</style>
<h1>🌱 CRCER - Tu ahorro con poco riesgo 🌱</h1>
""", unsafe_allow_html=True)


# Paso 2: Crear un formulario centrado en la página principal para recoger información del usuario
st.header("🛡️ Visualización de Inversión en Siefore de CRCER")
col1, col2, col3 = st.columns([1,1,1])

with col2:  # Usar la columna central para los inputs
    monto_inversion = st.number_input("💲 Cantidad a invertir inicialmente:", min_value=0, step=1000, key="inversion")
    monto_aportacion = st.number_input("📆 ¿De cuánto serán tus aportaciones mensuales?", min_value=0, step=100, key="aportacion")
    enfoque_inversion = st.selectbox("📝 ¿Cuál es tu edad?", ["20-30 años", "31-40 años", "41-50 años", "51+ años"])

# Guardar los valores de entrada en session_state para su uso en otros lugares del script
st.session_state['monto_inversion'] = monto_inversion
st.session_state['monto_aportacion'] = monto_aportacion

# PASO 3: Definir las variables de acciones y sus pesos globalmente
acciones = ['AC.MX', 'GCARSOA1.MX', 'GRUMAB.MX', 'ALSEA.MX', 'GAPB.MX', 'ASURB.MX', 'VOO', 'SPY']
pesos = [15.4, 5.00, 5.00, 5.00, 20.00, 12.1, 20.00, 17.5]  # Porcentajes como valores decimales

# Colocar el botón en el centro y asegurar la disposición correcta de los elementos visuales
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button('Visualizar Mi Inversión 💼'):
        # Asegurar que monto_inversion y monto_aportacion estén inicializados
        monto_inversion = st.session_state.get('monto_inversion', 0)
        monto_aportacion = st.session_state.get('monto_aportacion', 0)

        # Subpaso 1: Calcular la suma de la inversión inicial y la aportación mensual
        total_inversion = monto_inversion + monto_aportacion
        st.write(f'Esta es tu inversión hasta el momento: ${total_inversion}')

        # Subpaso 2: Crear un gráfico de pie con la distribución de la inversión en acciones
        inversion_por_accion = [total_inversion * peso / 100 for peso in pesos]
        fig_pie = px.pie(names=acciones, values=inversion_por_accion)
        st.write("## ➗ Distribución de tus inversiones")
        st.plotly_chart(fig_pie, use_container_width=True)

        # Subpaso 3: Gráfica de comparación de los últimos 10 años de nuestro portafolio con la inflación
        df = pd.read_csv('comparacion.csv')
        fig_line = px.line(df, x='Fecha', y=['Inflacion', 'CRCER'], labels={'value': 'Valor', 'variable': 'Índice'})
        st.write("## 💹 Cómo hubiera sido Inversión CRCER vs la tasa de inflación")
        st.plotly_chart(fig_line, use_container_width=True)

        # Subpaso 4: Proyección de crecimiento de las aportaciones anuales
        aportacion_anual = monto_aportacion * 12  # Convertir aportación mensual a anual
        rendimiento_anual = 0.1389  # Tasa de rendimiento anual de 13.89%
        volatilidad = 0.1336
        anos = list(range(2024, 2061))  # Años desde 2024 hasta 2070
        saldo = [aportacion_anual]  # Iniciar con la primera aportación anual
        for i in range(1, len(anos)):
            saldo.append(saldo[-1] * (1 + rendimiento_anual))  # Aplicar rendimiento y agregar nueva aportación

        fig_crecimiento = go.Figure()
        fig_crecimiento.add_trace(go.Scatter(x=anos, y=saldo, mode='lines+markers', name='Crecimiento de Inversión',
                                             line=dict(color='blue', width=2), marker=dict(color='blue', size=5)))
        fig_crecimiento.update_layout(title="Mira cómo se verían tus inversiones año con año!, esto toma en cuenta la volatilidad del portafolio",
                                      xaxis_title='Año', yaxis_title='Monto Acumulado ($)',
                                      template='plotly_dark')
        st.write("## 📈 ¡Cómo se verían mis inversiones?")
        st.plotly_chart(fig_crecimiento, use_container_width=True)

        # Subpaso 5: Mostrar el monto final en 2070 en una tabla
        monto_final = saldo[-1]  # Último valor del saldo
        df_final = pd.DataFrame({'Año': [2060], 'Monto Acumulado ($)': [monto_final], "Rendimiento anual":[14.81]})
        df_2 = pd.DataFrame({'Volatilidad Anual': [13.36], 'TIIE (4/29/2025)': [11.4029]})
        combinacion_df = pd.concat([df_final, df_2], axis=1)
        st.write("## 📈 Monto Acumulado en 2060")
        st.table(combinacion_df)

#Subpaso 6:
def calcular_crecimiento_inversion(aportacion_anual, rendimiento_anual, volatilidad):
    anos = list(range(2024, 2061))
    saldo = [aportacion_anual]  # Iniciar con la primera aportación anual
    for _ in range(1, len(anos)):
        # Aplicar rendimiento ajustado por volatilidad y agregar nueva aportación
        saldo.append(saldo[-1] * (1 + rendimiento_anual - volatilidad) + aportacion_anual)
    return anos, saldo

acciones = ['AC.MX', 'GCARSOA1.MX', 'GRUMAB.MX', 'ALSEA.MX', 'GAPB.MX', 'ASURB.MX', 'VOO', 'SPY']
pesos = [15.4, 5.00, 5.00, 5.00, 20.00, 12.1, 20.00, 17.5]

with st.form("form_inversion"):
    rendimiento_anual = st.slider("Tasa de Rendimiento Anual (%)", min_value=0.0, max_value=20.0, value=14.81, step=0.01, key="rendimiento")
    volatilidad = st.slider("Volatilidad Anual (%)", min_value=0.0, max_value=30.0, value=3.36, step=0.01, key="volatilidad")
    aportacion_mensual = st.number_input("Aportación Mensual ($)", min_value=0, max_value=100000, step=100, value=1000)
    submitted = st.form_submit_button("Actualizar Inversión")

if submitted:
    aportacion_anual = aportacion_mensual * 12  # Convertir aportación mensual a anual
    anos, saldo = calcular_crecimiento_inversion(aportacion_anual, rendimiento_anual / 100, volatilidad / 100)

    fig = go.Figure(go.Scatter(x=anos, y=saldo, mode='lines', name='Crecimiento de Inversión'))
    fig.update_layout(title="Simulación del Crecimiento de la Inversión Ajustada por Volatilidad",
                      xaxis_title='Año', yaxis_title='Monto Acumulado ($)',
                      template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

    st.write("## Detalles de la Inversión")
    st.write(f"- Volatilidad Anual: {volatilidad:.2f}%")
    st.write(f"- Rendimiento Anual: {rendimiento_anual:.2f}%")
    df_acciones = pd.DataFrame({'Acciones': acciones, 'Pesos (%)': pesos})
    st.write("### Distribución de Acciones y Pesos")
    st.table(df_acciones)
