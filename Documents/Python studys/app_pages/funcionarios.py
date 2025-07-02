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

# Função principal que exibe a página de funcionários
def show():
    # Verifica permissão antes de exibir a página
    if not usuario_tem_permissao("remover_funcionario"):
        st.error("Você não tem permissão para acessar esta página.")
        st.stop()
    st.title("👥 Funcionários")
    DATA_DIR = "data"
    ARQ_FUNCIONARIOS = os.path.join(DATA_DIR, "funcionarios.json")
    funcionarios = carregar_dados(ARQ_FUNCIONARIOS)
    count_func = len(funcionarios)
    # Abas para cadastro e gerenciamento
    aba = st.tabs([
        f"➕ Cadastrar Funcionário",
        f"👥 Gerenciar Funcionários ({count_func})"
    ])
    # --- Aba Cadastro ---
    with aba[0]:
        st.markdown("<h3 style='color:#1976d2;margin-bottom:16px;'>➕ Cadastrar Funcionário</h3>", unsafe_allow_html=True)
        with st.form("form_funcionario"):
            nome = st.text_input("Nome")
            funcao = st.selectbox("Função", ["Costureiro(a)", "Cortador(a)", "Revisor(a)"])
            telefone = st.text_input("Telefone")
            submit = st.form_submit_button("Cadastrar Funcionário")
            if submit:
                # Validação simples
                if nome.strip() and funcao.strip() and telefone.strip():
                    novo = {"nome": nome.strip(), "funcao": funcao, "telefone": telefone.strip()}
                    funcionarios.append(novo)
                    salvar_dados(ARQ_FUNCIONARIOS, funcionarios)
                    st.success("Funcionário cadastrado!")
                    st.rerun()
                else:
                    st.error("Preencha todos os campos.")
    # --- Aba Gerenciar ---
    with aba[1]:
        st.markdown(f"<h3 style='color:#1976d2;margin-bottom:12px;'>👥 Funcionários Cadastrados <span style='font-size:0.8em;color:#888'>({count_func})</span></h3>", unsafe_allow_html=True)
        for i, f in enumerate(funcionarios):
            cols = st.columns([6,1])
            # Exibe dados do funcionário
            cols[0].write(f"**{f['nome']}** — {f['funcao']} — {f['telefone']}")
            # Botão para remover funcionário
            if cols[1].button("Remover", key=f"del_func_{i}"):
                funcionarios.pop(i)
                salvar_dados(ARQ_FUNCIONARIOS, funcionarios)
                st.success("Funcionário removido!")
                st.rerun()
            # Linha divisória visual
            st.markdown("<hr style='margin: 8px 0; border: 0; border-top: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
