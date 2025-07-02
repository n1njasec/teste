import streamlit as st
from utils.json_utils import carregar_dados, salvar_dados
import os
import json

def show():
    st.title("🏷️ Tipos de Produto")
    DATA_DIR = "data"
    TIPOS_PRODUTO_PATH = os.path.join(DATA_DIR, "tipos_produto.json")
    # Função interna para carregar tipos de produto do arquivo
    def carregar_tipos_produto():
        if not os.path.exists(TIPOS_PRODUTO_PATH):
            with open(TIPOS_PRODUTO_PATH, 'w', encoding='utf-8') as f:
                json.dump(["Camiseta", "Bermuda", "Calça", "Outro"], f)
        with open(TIPOS_PRODUTO_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    # Função interna para salvar tipos de produto no arquivo
    def salvar_tipos_produto(tipos):
        with open(TIPOS_PRODUTO_PATH, 'w', encoding='utf-8') as f:
            json.dump(tipos, f, ensure_ascii=False, indent=4)
    st.markdown("Gerencie os tipos de produto disponíveis para cadastro de novos produtos.")
    st.markdown("---")
    with st.form("form_add_tipo_produto"):
        novo_tipo = st.text_input("Novo tipo de produto", max_chars=30)
        submit_tipo = st.form_submit_button("Adicionar tipo")
        tipos_produto = carregar_tipos_produto()
        if submit_tipo:
            if novo_tipo.strip() and novo_tipo not in tipos_produto:
                tipos_produto.append(novo_tipo.strip())
                salvar_tipos_produto(tipos_produto)
                st.success(f"Tipo '{novo_tipo}' adicionado!")
                st.rerun()
            elif novo_tipo in tipos_produto:
                st.warning("Tipo já existe.")
            else:
                st.warning("Digite um nome válido.")
    st.markdown("---")
    # Lista todos os tipos de produto cadastrados
    tipos_produto = carregar_tipos_produto()
    for i, tipo in enumerate(tipos_produto):
        col1, col2 = st.columns([6,1])
        with col1:
            st.markdown(f"<div style='display:flex; align-items:center; height:38px; font-size:1.1em; padding-left:8px;'><b>{tipo}</b></div>", unsafe_allow_html=True)
    # ...restante do código da página...
