import streamlit as st
from app_pages.login import load_users
import json
import os

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

# Função principal da página financeira
def show():
    # Verifica permissão de acesso à página
    if not usuario_tem_permissao("acessar_financeiro"):
        st.error("Você não tem permissão para acessar esta página.")
        st.stop()
    st.title("💰 Visão Geral Financeira")
    st.info("Aqui será exibido o resumo financeiro da empresa.")
    st.markdown("---")
    # Seções condicionais conforme permissões específicas
    if usuario_tem_permissao("ver_contas_receber"):
        st.title("📥 Contas a Receber")
        st.info("Aqui será possível gerenciar as contas a receber.")
        st.markdown("---")
    if usuario_tem_permissao("ver_contas_pagar"):
        st.title("📤 Contas a Pagar")
        st.info("Aqui será possível gerenciar as contas a pagar.")
        st.markdown("---")
    if usuario_tem_permissao("ver_fluxo_caixa"):
        st.title("💹 Fluxo de Caixa")
        st.info("Aqui será possível visualizar e gerenciar o fluxo de caixa.")
        st.markdown("---")
    if usuario_tem_permissao("ver_relatorios_financeiros"):
        st.title("📑 Relatórios Financeiros")
        st.info("Aqui será possível gerar relatórios financeiros.")
    # Recomenda-se comentar cada bloco de lógica adicional conforme expandir o arquivo
# Fim do arquivo financeiro.py
