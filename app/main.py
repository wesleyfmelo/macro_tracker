import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Macro Tracker",
    page_icon="📈",
    layout="wide"
)

# Conexão com o banco local
@st.cache_data(ttl=300)
def load_data():
    # Ajuste o caminho caso precise apontar para data/macro_database.db
    conn = sqlite3.connect(".\\data\\macro_database.db")
    query = "SELECT data, indicador, valor FROM indicadores ORDER BY data ASC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    df["data"] = pd.to_datetime(df["data"])
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    return df

def main():
    st.title("📈 Macro Tracker - Visão Geral")
    st.caption("Painel Macroeconômico Integrado")

    try:
        df = load_data()
        if df.empty:
            st.warning("Banco de dados vazio. Execute o pipeline para popular os dados.")
        else:
            st.success(f"Base carregada com sucesso! Total de registros: {len(df)}")
            st.info("Utilize o menu lateral para navegar entre as páginas temáticas.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

if __name__ == "__main__":
    main()