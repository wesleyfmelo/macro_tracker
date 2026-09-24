import streamlit as st
import pandas as pd

def render_metric_cards(df: pd.DataFrame, indicadores: list):
    """
    Renderiza os cartões de métricas superiores para os indicadores selecionados.
    """
    if not indicadores or df.empty:
        return

    cols = st.columns(len(indicadores))
    for i, ind in enumerate(indicadores):
        df_ind = df[df["indicador"] == ind]
        if not df_ind.empty:
            ultimo_registro = df_ind.iloc[-1]
            ultimo_valor = ultimo_registro["valor"]
            data_ultima = pd.to_datetime(ultimo_registro["data"]).strftime("%d/%m/%Y")
            
            # Variação em relação ao registro anterior (se existir)
            delta_str = None
            if len(df_ind) > 1:
                penultimo_valor = df_ind.iloc[-2]["valor"]
                delta = ultimo_valor - penultimo_valor
                delta_str = f"{delta:+.2f}"

            cols[i % len(cols)].metric(
                label=f"{ind} ({data_ultima})",
                value=f"{ultimo_valor:,.2f}",
                delta=delta_str
            )