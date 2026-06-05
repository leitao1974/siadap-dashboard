import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SIADAP 2026", layout="wide")
st.title("📊 Monitorização de Objetivos SIADAP 2026")

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTt48fFQi9XDLxOhlR1CGHPizyglJNEXCukIxWpN3_lN6d5aBiwuHxAPJbI8apqCmq8thF4XA6H0haN/pub?gid=2058887131&single=true&output=csv"

@st.cache_data(ttl=600)
def load_data():
    # Carrega os dados, ignorando linhas vazias se necessário
    return pd.read_csv(SHEET_URL)

try:
    df = load_data()
    
    # Limpeza: remover linhas onde 'Objetivo' seja nulo (comum em exports CSV do Sheets)
    df = df.dropna(subset=['Objetivo'])
    
    # Exibir a tabela
    st.write("Estado atual dos objetivos:")
    st.dataframe(df, use_container_width=True)
    
    # Gráfico
    fig = px.bar(df, x='Objetivo', y='Métrica Atual', color='Status',
                 color_discrete_map={'Verde': '#2ecc71', 'Amarelo': '#f1c40f', 'Vermelho': '#e74c3c'},
                 title="Progresso por Objetivo")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar: {e}. Verifica se o link CSV está correto e público.")
