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

# Mostrar el logo de CRCER centrado
st.markdown("""
<div style="text-align: center;">
    <img src="crcer.png" width="500">
</div>
""", unsafe_allow_html=True)

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
    monto_inversion = st.number_input("💲 Cantidad a invertir inicialmente:", min_value=0, step=1000, key="inversion")
    monto_aportacion = st.number_input("📆 ¿De cuánto serán tus aportaciones mensuales?", min_value=0, step=100, key="aportacion")
    enfoque_inversion = st.selectbox("📝 ¿Cuál es tu edad?", ["20-30 años", "31-40 años", "41-50 años", "51+ años"])

# Guardar los valores de entrada en session_state para su uso en otros lugares del script
st.session_state['monto_inversion'] = monto_inversion
st.session_state['monto_aportacion'] = monto_aportacion

# PASO 3 y PASO 4: Definir las variables de acciones y sus pesos globalmente y interacción con botón y visualización de la inversión
acciones = ['AC.MX', 'GCARSOA1.MX', 'GRUMAB.MX', 'ALSEA.MX', 'GAPB.MX', 'ASURB.MX', 'DIA', 'SPY']
pesos = [18.41, 5.00, 5.00, 5.00, 20.00, 11.77, 14.82, 20.00]  # Porcentajes como valores decimales

# Colocar el botón en el centro
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button('Visualizar Mi Inversión 💼'):
        col1, col2 = st.columns(2)
        with col1:
            # Asegurar que monto_inversion y monto_aportacion estén inicializados
            monto_inversion = st.session_state.get('monto_inversion', 0)
            monto_aportacion = st.session_state.get('monto_aportacion', 0)

            # Subpaso 1: Calcular la suma de la inversión inicial y la aportación mensual
            total_inversion = monto_inversion + monto_aportacion
            st.write(f'Esta es tu inversión total hasta el momento: ${total_inversion}')

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

            # Subpaso 4: Proyección de crecimiento de las aportaciones anuales
            aportacion_anual = monto_aportacion * 12  # Convertir aportación mensual a anual
            rendimiento_anual = 0.1481  # Tasa de rendimiento anual de 14.81%
            anos = list(range(2024, 2071))  # Años desde 2024 hasta 2070
            saldo = [aportacion_anual]  # Iniciar con la primera aportación anual
            for i in range(1, len(anos)):
                saldo.append(saldo[-1] * (1 + rendimiento_anual) + aportacion_anual)  # Aplicar rendimiento y agregar nueva aportación

            fig_crecimiento = go.Figure()
            fig_crecimiento.add_trace(go.Scatter(x=anos, y=saldo, mode='lines+markers', name='Crecimiento de Inversión',
                                                 line=dict(color='blue', width=2), marker=dict(color='red', size=5)))
            fig_crecimiento.update_layout(title="Mira cómo se verían tus inversiones año con año!",
                                          xaxis_title='Año', yaxis_title='Monto Acumulado ($)',
                                          template='plotly_dark')
            st.write("## Proyección de Crecimiento de la Inversión con CRCER 📥")
            st.plotly_chart(fig_crecimiento)

            # Subpaso 6: Mostrar el monto final en 2070 en una tabla
            monto_final = saldo[-1]  # Último valor del saldo
            df_final = pd.DataFrame({'Año': [2070], 'Monto Acumulado ($)': [monto_final]})
            st.write("## Monto Acumulado en 2070")
            st.table(df_final)
