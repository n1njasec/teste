import streamlit as st
import json
import os
from app_pages.login import load_users, save_users, hash_password

# Carrega lista de níveis e permissões do arquivo JSON
def load_niveis():
    path = os.path.join("data", "niveis.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Salva lista de níveis e permissões no arquivo JSON
def save_niveis(niveis):
    path = os.path.join("data", "niveis.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(niveis, f, ensure_ascii=False, indent=2)

# Painel administrativo principal
# Possui abas para gerenciar contas, níveis/permissões e senhas
def show_admin():
    st.title("\u2699\ufe0f Painel Administrativo")
    aba = st.tabs(["Gerenciar Contas", "Níveis e Permissões", "Senhas"])

    # --- Gerenciar Contas ---
    with aba[0]:
        st.subheader("Usuários Cadastrados")
        users = load_users()
        for i, u in enumerate(users):
            col1, col2, col3 = st.columns([4,2,1])
            col1.write(f"**{u['usuario']}** — {u['nivel']}")
            # Botão para remover usuário
            if col2.button("Remover", key=f"del_user_{i}"):
                users.pop(i)
                save_users(users)
                st.success("Usuário removido!")
                st.rerun()
        st.markdown("---")
        st.subheader("Criar Novo Usuário")
        novo_user = st.text_input("Novo usuário", key="novo_user")
        nova_senha = st.text_input("Senha", type="password", key="nova_senha")
        niveis = [n['nome'] for n in load_niveis()]
        nivel = st.selectbox("Nível", niveis, key="nivel_user")
        # Botão para criar novo usuário
        if st.button("Criar Usuário"):
            if novo_user and nova_senha:
                users.append({"usuario": novo_user, "senha": hash_password(nova_senha), "nivel": nivel})
                save_users(users)
                st.success("Usuário criado!")
                st.rerun()
            else:
                st.error("Preencha todos os campos.")

    # --- Níveis e Permissões ---
    with aba[1]:
        st.subheader("Gerenciar Níveis e Permissões")
        niveis = load_niveis()
        # Lista completa de permissões possíveis
        permissoes_possiveis = [
            "gerenciar_usuarios", "gerenciar_niveis", "gerenciar_senhas",
            "remover_produto", "remover_funcionario", "acessar_financeiro", "acessar_dashboard",
            "ver_contas_receber", "ver_contas_pagar", "ver_fluxo_caixa", "ver_relatorios_financeiros",
            "editar_produto", "editar_funcionario", "cadastrar_produto", "cadastrar_funcionario",
            "cadastrar_producao", "remover_producao", "editar_producao",
            "visualizar_estoque", "ajustar_estoque", "exportar_excel", "visualizar_relatorios",
            "acessar_tipos_produto", "remover_tipo_produto", "editar_tipo_produto"
        ]
        for i, n in enumerate(niveis):
            with st.expander(f"Nível: {n['nome']}"):
                # Multiselect para editar permissões do nível
                default_perms = [p for p in n['permissoes'] if p in permissoes_possiveis]
                novas_perms = st.multiselect(
                    f"Permissões para {n['nome']}", permissoes_possiveis, default=default_perms, key=f"perms_{i}")
                if st.button("Salvar Permissões", key=f"save_perms_{i}"):
                    niveis[i]['permissoes'] = novas_perms
                    save_niveis(niveis)
                    st.success("Permissões atualizadas!")
                    st.rerun()
                # Só permite remover níveis customizados
                if n['nome'] not in ["admin", "comum"]:
                    if st.button("Remover Nível", key=f"del_nivel_{i}"):
                        niveis.pop(i)
                        save_niveis(niveis)
                        st.success("Nível removido!")
                        st.rerun()
        st.markdown("---")
        st.subheader("Criar Novo Nível")
        novo_nivel = st.text_input("Nome do novo nível", key="novo_nivel")
        novas_perms = st.multiselect("Permissões", permissoes_possiveis, key="perms_novo")
        if st.button("Criar Nível"):
            if novo_nivel and novas_perms:
                if novo_nivel in [n['nome'] for n in niveis]:
                    st.error("Nível já existe.")
                else:
                    niveis.append({"nome": novo_nivel, "permissoes": novas_perms})
                    save_niveis(niveis)
                    st.success("Nível criado!")
                    st.rerun()
            else:
                st.error("Preencha todos os campos.")

    # --- Gerenciamento de Senhas ---
    with aba[2]:
        st.subheader("Redefinir Senha de Usuário")
        users = load_users()
        user_list = [u["usuario"] for u in users]
        user_sel = st.selectbox("Usuário", user_list, key="user_reset")
        new_pass = st.text_input("Nova senha", type="password", key="new_pass")
        # Botão para redefinir senha
        if st.button("Redefinir Senha"):
            for u in users:
                if u["usuario"] == user_sel:
                    u["senha"] = hash_password(new_pass)
                    save_users(users)
                    st.success("Senha redefinida!")
                    st.rerun()
