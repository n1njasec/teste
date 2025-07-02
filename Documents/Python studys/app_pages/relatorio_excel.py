import streamlit as st
import pandas as pd
from utils.json_utils import carregar_dados
import os
import json

# Carrega os níveis de permissão do arquivo JSON
def load_niveis():
    path = os.path.join("data", "niveis.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Verifica se o usuário logado possui determinada permissão
def usuario_tem_permissao(permissao):
    if "nivel" not in st.session_state:
        return False
    niveis = load_niveis()
    nivel_usuario = st.session_state["nivel"]
    nivel = next((n for n in niveis if n["nome"] == nivel_usuario), None)
    if not nivel:
        return False
    return permissao in nivel["permissoes"]

# Função principal da página de exportação de produções para Excel
def show():
    # Verifica permissão de acesso à página
    if not usuario_tem_permissao("acessar_dashboard"):
        st.error("Você não tem permissão para acessar esta página.")
        st.stop()
    st.title("📊 Exportar Produções para Excel")
    DATA_DIR = "data"
    ARQ_PRODUCOES = os.path.join(DATA_DIR, "producoes.json")
    producoes = carregar_dados(ARQ_PRODUCOES)
    # Instruções de uso
    st.markdown("""
    <div style='background-color:#e3f2fd; padding:12px 18px; border-radius:8px; margin-bottom:18px;'>
        <b>Como usar:</b> Utilize os filtros abaixo para selecionar as produções desejadas e clique em <b>Baixar Excel filtrado</b>.<br>
        O arquivo gerado pode ser aberto no Excel ou Google Planilhas.
    </div>
    """, unsafe_allow_html=True)
    if not producoes:
        st.info("Nenhuma produção para exportar.")
        return
    # Cria DataFrame com os dados das produções
    df = pd.DataFrame(producoes)
    status_opcoes = ["Todos"] + sorted(df["status"].unique().tolist())
    produto_opcoes = ["Todos"] + sorted(df["produto_nome"].unique().tolist())
    # Filtros para exportação
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
    # Exibe quantidade de registros filtrados
    st.markdown(f"<b>Registros encontrados:</b> <span style='color:#1976d2;font-size:1.2em'>{len(df_filtrado)}</span>", unsafe_allow_html=True)
    # Exibe tabela filtrada
    st.dataframe(df_filtrado[["lote", "produto_codigo", "produto_nome", "funcionario_nome", "funcionario_funcao", "quantidade", "status", "data"]], use_container_width=True)
    # O botão de download pode ser implementado conforme necessidade
    # Recomenda-se comentar cada bloco de lógica adicional conforme expandir o arquivo
# Fim do arquivo relatorio_excel.py
