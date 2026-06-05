import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Monitorização SIADAP 2026", layout="wide")

# Link do CSV (o teu link do Sheets)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTt48fFQi9XDLxOhlR1CGHPizyglJNEXCukIxWpN3_lN6d5aBiwuHxAPJbI8apqCmq8thF4XA6H0haN/pub?gid=2058887131&single=true&output=csv"

@st.cache_data(ttl=600)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.replace(r'[^\w\s]', '', regex=True).str.strip()
    return df

try:
    df = load_data()
    
    st.title("📊 Monitorização de Objetivos SIADAP 2026")
    
    # 1. CÁLCULO DINÂMICO: Contar IDs por Objetivo
    # Isto assume que cada linha no teu Sheets é um processo com um ID
    contagem_processos = df.groupby('Objetivo')['ID'].count().reset_index()
    contagem_processos.columns = ['Objetivo', 'Nº de Processos']

    # Layout: Colunas para o Gráfico e a Tabela de Contagem
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Progresso por Objetivo")
        fig = px.bar(df, x='Objetivo', y='Métrica Atual', color='Status', ...)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Volume de Processos")
        # Apresenta a contagem calculada pelo algoritmo
        st.table(contagem_processos)

except Exception as e:
    st.error(f"Erro: {e}")
