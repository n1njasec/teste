import streamlit as st
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

# Função principal da página de estoque
def show():
    # Verifica permissão de acesso à página
    if not usuario_tem_permissao("acessar_dashboard"):
        st.error("Você não tem permissão para acessar esta página.")
        st.stop()
    st.title("📦 Visão Geral do Estoque")
    st.info("Aqui será exibido o resumo do estoque.")
    st.markdown("---")
    # Seções para entrada, saída e ajuste de estoque
    st.title("➕ Entrada de Produtos")
    st.info("Aqui será possível registrar entradas de produtos no estoque.")
    st.markdown("---")
    st.title("➖ Saída de Produtos")
    st.info("Aqui será possível registrar saídas de produtos do estoque.")
    st.markdown("---")
    st.title("✏️ Ajuste Manual de Estoque")
    st.info("Aqui será possível ajustar manualmente o saldo de estoque.")
    st.markdown("---")
    st.title("📊 Relatório de Estoque")
    st.info("Aqui será possível gerar relatórios de estoque.")
    # Recomenda-se comentar cada bloco de lógica adicional conforme expandir o arquivo
# Fim do arquivo estoque.py
