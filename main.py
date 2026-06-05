import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Monitorização SIADAP 2026", layout="wide")

st.title("📊 Monitorização de Objetivos SIADAP 2026")

# Link do teu CSV publicado
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTt48fFQi9XDLxOhlR1CGHPizyglJNEXCukIxWpN3_lN6d5aBiwuHxAPJbI8apqCmq8thF4XA6H0haN/pubhtml?gid=2058887131&single=true"

@st.cache_data(ttl=600)
def load_data():
    return pd.read_csv(CSV_URL)

try:
    df = load_data()
    st.write("Dados atualizados com sucesso!")
    
    # Exemplo de Gráfico
    fig = px.bar(df, x='Objetivo', y='Valor', color='Status', 
                 title="Progresso dos Objetivos")
    st.plotly_chart(fig, use_container_width=True)
    
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
