import streamlit as st
from streamlit_option_menu import option_menu
from app_pages import produtos, funcionarios, producoes, tipos_produto, estoque, financeiro, dashboard, relatorio_excel, login, admin
import os

# --- Login temporariamente desativado ---
# if "usuario" not in st.session_state:
#     login.show_login()
#     st.stop()

# --- Menu lateral ---
with st.sidebar:
    # Saudação personalizada
    st.title(f"👋 Olá, {st.session_state.get('usuario', 'Usuário')}")
    st.markdown("---")
    # Menu principal com ícones e navegação
    menu_lateral = option_menu(
        "Menu",
        [
            "Dashboard", "Produtos", "Funcionários", "Produções", "Tipos de Produto",
            "Estoque", "Financeiro", "Relatório Excel", "Painel Admin", "Sair"
        ],
        icons=[
            'house', 'box', 'people', 'gear', 'tag', 'archive', 'bar-chart',
            'file-earmark-excel', 'tools', 'box-arrow-right'
        ],
        menu_icon="cast",
        default_index=0,
    )
    st.markdown("---")

# --- Roteamento das páginas ---
# Painel Admin só para administradores
if menu_lateral == "Painel Admin":
    if st.session_state.get("nivel") == "admin":
        admin.show_admin()
    else:
        st.error("Acesso restrito ao administrador.")
    st.stop()

# Logout
if menu_lateral == "Sair":
    login.logout()
    st.stop()

# Chama a página correspondente conforme a opção escolhida
if menu_lateral == "Dashboard":
    dashboard.show()
elif menu_lateral == "Produtos":
    produtos.show()
elif menu_lateral == "Funcionários":
    funcionarios.show()
elif menu_lateral == "Produções":
    producoes.show()
elif menu_lateral == "Tipos de Produto":
    tipos_produto.show()
elif menu_lateral == "Estoque":
    estoque.show()
elif menu_lateral == "Financeiro":
    financeiro.show()
elif menu_lateral == "Relatório Excel":
    relatorio_excel.show()

# --- DEBUG: Lista arquivos do diretório do projeto ---
with st.expander("DEBUG: Arquivos do projeto"):
    for root, dirs, files in os.walk("."):
        for name in files:
            st.write(os.path.join(root, name))
