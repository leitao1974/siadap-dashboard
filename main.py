import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Monitorização SIADAP 2026", layout="wide")
st.title("📊 Monitorização de Objetivos SIADAP 2026")

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTt48fFQi9XDLxOhlR1CGHPizyglJNEXCukIxWpN3_lN6d5aBiwuHxAPJbI8apqCmq8thF4XA6H0haN/pub?gid=2058887131&single=true&output=csv"

@st.cache_data(ttl=600)
def load_data():
    df = pd.read_csv(SHEET_URL)
    # Limpeza profunda dos nomes das colunas
    df.columns = ['Objetivo', 'Metrica', 'Status']
    return df

try:
    df = load_data()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Progresso por Objetivo")
        fig = px.bar(df, x='Objetivo', y='Metrica', color='Status',
                     color_discrete_map={'Verde': '#2ecc71', 'Amarelo': '#f1c40f', 'Vermelho': '#e74c3c'})
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Tabela de Dados")
        # Exibe os dados exatamente como estão no Sheets
        st.table(df)
        
        # Informativo
        st.info("Nota: A tabela mostra os valores consolidados da aba Dashboard_Data.")

except Exception as e:
    st.error(f"Erro ao carregar: {e}")
