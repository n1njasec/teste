import streamlit as st
import hashlib
import json
import os

# Gera hash SHA-256 da senha para armazenamento seguro
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Carrega lista de usuários do arquivo JSON
def load_users():
    path = os.path.join("data", "usuarios.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Salva lista de usuários no arquivo JSON
def save_users(users):
    path = os.path.join("data", "usuarios.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# Exibe tela de login e faz autenticação
def show_login():
    st.title("🔐 Login")
    users = load_users()
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        # Busca usuário e valida senha (hash)
        user = next((u for u in users if u["usuario"] == username and u["senha"] == hash_password(password)), None)
        if user:
            st.session_state["usuario"] = user["usuario"]
            st.session_state["nivel"] = user["nivel"]
            st.success(f"Bem-vindo, {user['usuario']}!")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

# Realiza logout limpando sessão
def logout():
    for k in ["usuario", "nivel"]:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()
