import streamlit as st
import pandas as pd
from utils.json_utils import carregar_dados
import os
import json

def show():
    st.title("📊 Exportar Produções para Excel")
    DATA_DIR = "data"
    ARQ_PRODUCOES = os.path.join(DATA_DIR, "producoes.json")
    producoes = carregar_dados(ARQ_PRODUCOES)
    st.markdown("""
    <div style='background-color:#e3f2fd; padding:12px 18px; border-radius:8px; margin-bottom:18px;'>
        <b>Como usar:</b> Utilize os filtros abaixo para selecionar as produções desejadas e clique em <b>Baixar Excel filtrado</b>.<br>
        O arquivo gerado pode ser aberto no Excel ou Google Planilhas.
    </div>
    """, unsafe_allow_html=True)
    if not producoes:
        st.info("Nenhuma produção para exportar.")
        return
    df = pd.DataFrame(producoes)
    status_opcoes = ["Todos"] + sorted(df["status"].unique().tolist())
    produto_opcoes = ["Todos"] + sorted(df["produto_nome"].unique().tolist())
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            filtro_status = st.selectbox("Filtrar por Status", status_opcoes, key="filtro_status_excel")
        with col2:
            filtro_produto = st.selectbox("Filtrar por Produto", produto_opcoes, key="filtro_produto_excel")
    df_filtrado = df.copy()
    if filtro_status != "Todos":
        df_filtrado = df_filtrado[df_filtrado["status"] == filtro_status]
    if filtro_produto != "Todos":
        df_filtrado = df_filtrado[df_filtrado["produto_nome"] == filtro_produto]
    st.markdown(f"<b>Registros encontrados:</b> <span style='color:#1976d2;font-size:1.2em'>{len(df_filtrado)}</span>", unsafe_allow_html=True)
    st.dataframe(df_filtrado[["lote", "produto_codigo", "produto_nome", "funcionario_nome", "funcionario_funcao", "quantidade", "status", "data"]], use_container_width=True)
