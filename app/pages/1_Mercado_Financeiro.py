import sqlite3
import pandas as pd
import streamlit as st
from app.components.cards import render_metric_cards
from app.components.charts import render_line_chart

st.set_page_config(page_title="Mercado Financeiro", page_icon="💵", layout="wide")

@st.cache_data(ttl=300)
def load_data():
    conn = sqlite3.connect(".\\data\\macro_database.db")
    query = "SELECT data, indicador, valor FROM indicadores ORDER BY data ASC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    df["data"] = pd.to_datetime(df["data"])
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    return df

st.title("💵 Mercado Financeiro")

df = load_data()

# Filtrar apenas séries financeiras (Selic, Câmbio, CDI, etc.)
indicadores_fin = [ind for ind in df["indicador"].unique() if any(k in ind.upper() for k in ["SELIC", "CAMBIO", "CDI", "USD"])]

if not indicadores_fin:
    indicadores_fin = list(df["indicador"].unique())

st.sidebar.header("Filtros")
selecionados = st.sidebar.multiselect("Indicadores:", indicadores_fin, default=indicadores_fin[:2])

if selecionados:
    df_filtered = df[df["indicador"].isin(selecionados)]
    render_metric_cards(df_filtered, selecionados)
    st.markdown("---")
    render_line_chart(df_filtered, "Taxas de Juros e Câmbio")