import streamlit as st
from utils.json_utils import carregar_dados, salvar_dados
import os
import json

# Carrega os níveis de permissão a partir do arquivo JSON
def load_niveis():
    path = os.path.join("data", "niveis.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Verifica se o usuário tem a permissão necessária
def usuario_tem_permissao(permissao):
    if "nivel" not in st.session_state:
        return False
    niveis = load_niveis()
    nivel_usuario = st.session_state["nivel"]
    nivel = next((n for n in niveis if n["nome"] == nivel_usuario), None)
    if not nivel:
        return False
    return permissao in nivel["permissoes"]

# Função principal para exibir a página de produtos
def show():
    # Verifica permissão antes de exibir a página
    if not usuario_tem_permissao("remover_produto"):
        st.error("Você não tem permissão para acessar esta página.")
        st.stop()
    st.title("📦 Produtos")
    DATA_DIR = "data"
    ARQ_PRODUTOS = os.path.join(DATA_DIR, "produtos.json")
    produtos = carregar_dados(ARQ_PRODUTOS)
    count_prod = len(produtos)
    # Abas para cadastro e gerenciamento
    aba = st.tabs([
        f"➕ Cadastrar Produto",
        f"📦 Gerenciar Produtos ({count_prod})"
    ])
    # --- Aba Cadastro ---
    with aba[0]:
        st.markdown("<h3 style='color:#1976d2;margin-bottom:16px;'>➕ Cadastrar Produto</h3>", unsafe_allow_html=True)
        with st.form("form_produto"):
            nome = st.text_input("Nome do Produto")
            codigo = st.text_input("Código")
            descricao = st.text_area("Descrição")
            tipo = st.text_input("Tipo")
            submit = st.form_submit_button("Cadastrar Produto")
            if submit:
                # Validação simples
                if nome.strip() and codigo.strip():
                    novo = {"nome": nome.strip(), "codigo": codigo.strip(), "descricao": descricao.strip(), "tipo": tipo}
                    produtos.append(novo)
                    salvar_dados(ARQ_PRODUTOS, produtos)
                    st.success("Produto cadastrado!")
                    st.rerun()
                else:
                    st.error("Preencha nome e código.")
    # --- Aba Gerenciar ---
    with aba[1]:
        st.markdown(f"<h3 style='color:#1976d2;margin-bottom:12px;'>📦 Produtos Cadastrados <span style='font-size:0.8em;color:#888'>({count_prod})</span></h3>", unsafe_allow_html=True)
        for i, p in enumerate(produtos):
            cols = st.columns([6,1])
            # Exibe dados do produto
            cols[0].write(f"**{p['nome']}** ({p['codigo']}) - {p['tipo']}")
            # Botão para remover produto
            if cols[1].button("Remover", key=f"del_prod_{i}"):
                produtos.pop(i)
                salvar_dados(ARQ_PRODUTOS, produtos)
                st.success("Produto removido!")
                st.rerun()
            # Linha divisória visual
            st.markdown("<hr style='margin: 8px 0; border: 0; border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
