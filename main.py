import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para visualização profissional
st.set_page_config(page_title="Monitorização SIADAP 2026", layout="wide")

# Título do Dashboard
st.title("📊 Monitorização de Objetivos SIADAP 2026")
st.markdown("---")

# URL do CSV publicado (substitui pelo teu link real)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTt48fFQi9XDLxOhlR1CGHPizyglJNEXCukIxWpN3_lN6d5aBiwuHxAPJbI8apqCmq8thF4XA6H0haN/pub?gid=2058887131&single=true&output=csv"

@st.cache_data(ttl=600)
def load_data():
    # Lê o CSV
    df = pd.read_csv(SHEET_URL)
    
    # Lógica de limpeza robusta:
    # 1. Remove espaços em branco dos nomes das colunas
    # 2. Remove caracteres invisíveis (como o carácter que causava o erro na célula A1)
    df.columns = df.columns.str.replace(r'[^\w\s]', '', regex=True).str.strip()
    
    # Renomeia forçosamente se necessário para garantir o sucesso do gráfico
    # Assumindo que a tua coluna 1 é Objetivo, 2 é Métrica Atual, 3 é Status
    df.columns = ['Objetivo', 'Métrica Atual', 'Status']
    
    return df

try:
    df = load_data()
    
    # Exibir métricas rápidas (KPIs)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Objetivos", len(df))
    
    # Exibir a tabela com formatação
    st.subheader("Estado Detalhado dos Objetivos")
    st.dataframe(df, use_container_width=True)
    
    # Gráfico de barras de progresso
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
        title="Progresso por Objetivo (SIADAP 2026)"
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao processar os dados: {e}")
    st.info("Dica: Verifica se o link do CSV no Sheets foi publicado corretamente e se as colunas são: Objetivo, Métrica Atual, Status.")
