import plotly.express as px
import pandas as pd
import streamlit as st

def render_line_chart(df: pd.DataFrame, title: str = "Evolução Temporal"):
    """
    Gera e exibe um gráfico de linhas interativo com Plotly.
    """
    if df.empty:
        st.info("Nenhum dado disponível para o período selecionado.")
        return

    fig = px.line(
        df,
        x="data",
        y="valor",
        color="indicador",
        title=title,
        labels={"data": "Data", "valor": "Valor", "indicador": "Indicador"},
        template="plotly_white"
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)