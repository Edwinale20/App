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

# Paso 3 se ha modificado para que no repita la visualización de la información
# Sólo necesitas incluirlo si quieres realizar alguna acción adicional con la información recogida

# PASO 4: Interacción con botón y visualización de la inversión

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
        # Asegurarse de que la lista de pesos es accesible y está definida
        if pesos:
            inversion_por_accion = [total_inversion * peso / 100 for peso in pesos]
            fig_pie = px.pie(names=acciones, values=inversion_por_accion, title="Distribución de la Inversión en Acciones")
            st.plotly_chart(fig_pie)

        # Subpaso 3: Gráfica de comparación de los últimos 10 años de nuestro portafolio con la TIIE
        df = pd.read_csv('comparacion.csv')  # Asegúrate de que el archivo está en el directorio correcto
        fig_line = px.line(df, x='Fecha', y=['TIIE', 'CRECR'], title='Comparación de la Inversión CRECR con TIIE 📈', labels={'value': 'Valor', 'variable': 'Índice'})
        st.plotly_chart(fig_line)

        # Visualizar la tabla de acciones y pesos en la segunda columna solo si el botón es presionado
        with col2:
            st.write("## Acciones y sus Pesos 📊")
            # Crear una tabla de datos para mostrar las acciones y pesos
            data = {'Acciones': acciones, 'Pesos (%)': pesos}
            df_acciones = pd.DataFrame(data)
            st.table(df_acciones)
