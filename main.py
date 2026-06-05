import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Monitorização SIADAP 2026", layout="wide")

# Título do Dashboard
st.title("📊 Monitorização de Objetivos SIADAP 2026")
st.markdown("---")

# O teu link oficial de publicação CSV
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTt48fFQi9XDLxOhlR1CGHPizyglJNEXCukIxWpN3_lN6d5aBiwuHxAPJbI8apqCmq8thF4XA6H0haN/pub?gid=2058887131&single=true&output=csv"

@st.cache_data(ttl=600)
def load_data():
    # Lê o CSV diretamente do teu Google Sheets
    df = pd.read_csv(SHEET_URL)
    
    # Limpeza robusta: Remove caracteres invisíveis e espaços dos cabeçalhos
    df.columns = df.columns.str.replace(r'[^\w\s]', '', regex=True).str.strip()
    
    # Renomeia forçosamente para garantir que o código encontra as colunas corretas
    df.columns = ['Objetivo', 'Métrica Atual', 'Status']
    
    return df

try:
    df = load_data()
    
    # Layout em duas colunas: Gráfico (à esquerda) e Tabela (à direita)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Progresso por Objetivo")
        fig = px.bar(
            df, 
            x='Objetivo', 
            y='Métrica Atual', 
            color='Status',
            color_discrete_map={
                'Verde': '#2ecc71', 
                'Amarelo': '#f1c40f', 
                'Vermelho': '#e74c3c'
            },
            title="Monitorização de Desempenho (CCDR Centro)"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Tabela de Resumo")
        # Exibe a tabela formatada
        st.table(df)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.info("Dica: Verifica se publicaste a aba 'Dashboard_Data' como CSV no Google Sheets.")
