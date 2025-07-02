import streamlit as st
from streamlit_option_menu import option_menu
from app_pages import produtos, funcionarios, producoes, tipos_produto, estoque, financeiro, dashboard, relatorio_excel, login, admin

# --- Login removido: qualquer um acessa tudo ---
# if "usuario" not in st.session_state:
#     login.show_login()
#     st.stop()

# --- Menu lateral ---
with st.sidebar:
    st.title("👋 Olá, visitante!")
    st.markdown("---")
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

# --- DEBUG: Lista arquivos do diretório do projeto ---
import os
with st.expander("DEBUG: Arquivos do projeto"):
    for root, dirs, files in os.walk("."):
        for name in files:
            st.write(os.path.join(root, name))

# --- Roteamento das páginas ---
# Painel Admin liberado para todos
if menu_lateral == "Painel Admin":
    admin.show_admin()
    st.stop()

# Logout (apenas volta para o início)
if menu_lateral == "Sair":
    st.experimental_rerun()
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
