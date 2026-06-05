import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Monitorização SIADAP 2026", layout="wide")

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTt48fFQi9XDLxOhlR1CGHPizyglJNEXCukIxWpN3_lN6d5aBiwuHxAPJbI8apqCmq8thF4XA6H0haN/pub?gid=2058887131&single=true&output=csv"

@st.cache_data(ttl=600)
def load_data():
    df = pd.read_csv(SHEET_URL)
    # Limpeza: remove caracteres especiais e espaços nos cabeçalhos
    df.columns = df.columns.str.replace(r'[^\w\s]', '', regex=True).str.strip()
    return df

st.title("📊 Monitorização de Objetivos SIADAP 2026")

try:
    df = load_data()
    
    # 1. Limpeza forçada dos nomes das colunas para corresponder ao que o código espera
    # Como o teu CSV tem cabeçalhos como "A (Objetivo)", vamos renomear aqui:
    df.columns = ['Objetivo', 'Metrica Atual', 'Status Semáforo']
    
    # 2. Cálculo da Tabela de Volume
    # Como não temos uma coluna ID na Dashboard_Data, usamos o próprio resumo para contar
    # Se quiseres contar processos reais, terias de ler os outros CSVs (Obj1, Obj2...)
    contagem = df[['Objetivo', 'Metrica Atual']]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Progresso por Objetivo")
        fig = px.bar(
            df, 
            x='Objetivo', 
            y='Metrica Atual', 
            color='Status Semáforo',
            color_discrete_map={'Verde': '#2ecc71', 'Amarelo': '#f1c40f', 'Vermelho': '#e74c3c'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Volume por Objetivo")
        st.table(contagem)

except Exception as e:
    st.error(f"Erro ao carregar ou processar dados: {e}")
