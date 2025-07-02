import streamlit as st
import pandas as pd
import plotly.express as px
from utils.json_utils import carregar_dados
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

# Função principal da página de dashboard
def show():
    # Verifica permissão de acesso à página
    if not usuario_tem_permissao("acessar_dashboard"):
        st.error("Você não tem permissão para acessar esta página.")
        st.stop()
    # Título e cabeçalho visual
    st.markdown("""
        <div style='display:flex;align-items:center;gap:18px;margin-bottom:18px;'>
            <img src='https://img.icons8.com/ios-filled/100/factory.png' width='48' style='margin-right:8px;'>
            <h1 style='color:#1976d2;margin:0;font-size:2.2em;'>Dashboard de Produção</h1>
        </div>
    """, unsafe_allow_html=True)
    # Carrega dados dos arquivos principais
    DATA_DIR = "data"
    ARQ_PRODUTOS = os.path.join(DATA_DIR, "produtos.json")
    ARQ_FUNCIONARIOS = os.path.join(DATA_DIR, "funcionarios.json")
    ARQ_PRODUCOES = os.path.join(DATA_DIR, "producoes.json")
    produtos = carregar_dados(ARQ_PRODUTOS)
    funcionarios = carregar_dados(ARQ_FUNCIONARIOS)
    producoes = carregar_dados(ARQ_PRODUCOES)
    # Calcula totais e contadores para os cards
    total_produtos = len(produtos)
    total_funcionarios = len(funcionarios)
    total_producoes = len(producoes)
    em_corte = len([p for p in producoes if p["status"] == "Cortando"])
    costurando = len([p for p in producoes if p["status"] == "Costurando"])
    revisando = len([p for p in producoes if p["status"] == "Revisando e Embalando"])
    concluidas = len([p for p in producoes if p["status"] == "Concluído"])
    # Cards principais de resumo
    st.markdown("""
    <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-bottom:18px;'>
        <div style='background:#e3f2fd;border-radius:14px;padding:18px 0;box-shadow:0 2px 12px #0001;text-align:center;'>
            <div style='font-size:2.2em;'>📦</div>
            <div style='font-size:1.1em;color:#1976d2;font-weight:600;'>Produtos</div>
            <div style='font-size:2em;font-weight:700;color:#222;'>{}</div>
        </div>
        <div style='background:#fff3e0;border-radius:14px;padding:18px 0;box-shadow:0 2px 12px #0001;text-align:center;'>
            <div style='font-size:2.2em;'>👥</div>
            <div style='font-size:1.1em;color:#ff9800;font-weight:600;'>Funcionários</div>
            <div style='font-size:2em;font-weight:700;color:#222;'>{}</div>
        </div>
        <div style='background:#e8f5e9;border-radius:14px;padding:18px 0;box-shadow:0 2px 12px #0001;text-align:center;'>
            <div style='font-size:2.2em;'>⚙️</div>
            <div style='font-size:1.1em;color:#43a047;font-weight:600;'>Produções</div>
            <div style='font-size:2em;font-weight:700;color:#222;'>{}</div>
        </div>
        <div style='background:#ede7f6;border-radius:14px;padding:18px 0;box-shadow:0 2px 12px #0001;text-align:center;'>
            <div style='font-size:2.2em;'>✅</div>
            <div style='font-size:1.1em;color:#7e57c2;font-weight:600;'>Concluídas</div>
            <div style='font-size:2em;font-weight:700;color:#222;'>{}</div>
        </div>
    </div>
    """.format(total_produtos, total_funcionarios, total_producoes, concluidas), unsafe_allow_html=True)
    # Cards de etapas do processo produtivo
    st.markdown("""
    <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-bottom:18px;'>
        <div style='background:#e3f2fd;border-radius:10px;padding:12px 0;text-align:center;'>
            <div style='font-size:1.5em;'>✂️ Cortando</div>
            <div style='font-size:1.6em;font-weight:700;color:#1976d2;'>{}</div>
        </div>
        <div style='background:#fff3e0;border-radius:10px;padding:12px 0;text-align:center;'>
            <div style='font-size:1.5em;'>🧵 Costurando</div>
            <div style='font-size:1.6em;font-weight:700;color:#ff9800;'>{}</div>
        </div>
        <div style='background:#e8f5e9;border-radius:10px;padding:12px 0;text-align:center;'>
            <div style='font-size:1.5em;'>📦 Revisando e Embalando</div>
            <div style='font-size:1.6em;font-weight:700;color:#43a047;'>{}</div>
        </div>
    </div>
    """.format(em_corte, costurando, revisando), unsafe_allow_html=True)
    # Aqui pode-se adicionar gráficos, tabelas ou outros elementos visuais conforme necessidade
    # Recomenda-se comentar cada bloco de lógica adicional conforme expandir o arquivo
# Fim do arquivo dashboard.py
