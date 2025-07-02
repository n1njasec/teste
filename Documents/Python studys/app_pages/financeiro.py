import streamlit as st
from app_pages.login import load_users
import json
import os

BASE_DIR = os.path.join(".", "Documents", "Python studys")

def show():
    st.title("💰 Visão Geral Financeira")
    st.info("Aqui será exibido o resumo financeiro da empresa.")
    st.markdown("---")
    st.title("📥 Contas a Receber")
    st.info("Aqui será possível gerenciar as contas a receber.")
    st.markdown("---")
    st.title("📤 Contas a Pagar")
    st.info("Aqui será possível gerenciar as contas a pagar.")
    st.markdown("---")
    st.title("💹 Fluxo de Caixa")
    st.info("Aqui será possível visualizar e gerenciar o fluxo de caixa.")
    st.markdown("---")
    st.title("📑 Relatórios Financeiros")
    st.info("Aqui será possível gerar relatórios financeiros.")
    # ...restante do código da página...
# Fim do arquivo financeiro.py
