import streamlit as st
from utils.json_utils import carregar_dados, salvar_dados
import os
import json
from datetime import datetime

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

# Função principal da página de produções
def show():
    # Verifica permissão de acesso à página
    if not usuario_tem_permissao("acessar_dashboard"):
        st.error("Você não tem permissão para acessar esta página.")
        st.stop()
    st.title("⚙️ Produções")
    # Define caminhos dos arquivos de dados
    DATA_DIR = "data"
    ARQ_PRODUCOES = os.path.join(DATA_DIR, "producoes.json")
    ARQ_FUNCIONARIOS = os.path.join(DATA_DIR, "funcionarios.json")
    ARQ_PRODUTOS = os.path.join(DATA_DIR, "produtos.json")
    # Carrega dados necessários
    producoes = carregar_dados(ARQ_PRODUCOES)
    funcionarios = carregar_dados(ARQ_FUNCIONARIOS)
    produtos = carregar_dados(ARQ_PRODUTOS)
    # Define etapas do processo produtivo
    status_etapas = ["Cortando", "Costurando", "Revisando e Embalando", "Concluído"]
    etapa_icones = {
        "Cortando": "✂️",
        "Costurando": "🧵",
        "Revisando e Embalando": "📦",
        "Concluído": "✅"
    }
    etapa_cores = {
        "Cortando": "#e3f2fd",
        "Costurando": "#fff3e0",
        "Revisando e Embalando": "#e8f5e9",
        "Concluído": "#ede7f6"
    }
    # Contadores para cada etapa
    counts = {etapa: len([p for p in producoes if p["status"] == etapa]) for etapa in status_etapas}
    # Cria abas para cada etapa do processo
    aba = st.tabs([
        "➕ Nova Produção",
        f"{etapa_icones['Cortando']} Cortando ({counts['Cortando']})",
        f"{etapa_icones['Costurando']} Costurando ({counts['Costurando']})",
        f"{etapa_icones['Revisando e Embalando']} Revisando e Embalando ({counts['Revisando e Embalando']})",
        f"{etapa_icones['Concluído']} Concluídos ({counts['Concluído']})"
    ])
    # --- Aba Nova Produção ---
    with aba[0]:
        st.markdown("<h3 style='color:#1976d2;margin-bottom:16px;'>➕ Nova Produção</h3>", unsafe_allow_html=True)
        # Geração automática do número de lote
        hoje = datetime.today()
        prefixo_lote = hoje.strftime("%d%m%y")
        sufixos = [int(p["lote"].split("/")[-1]) for p in producoes if p["lote"].startswith(prefixo_lote)]
        proximo_sufixo = max(sufixos) + 1 if sufixos else 1
        lote_gerado = f"{prefixo_lote}/{proximo_sufixo:03d}"
        # Formulário para cadastro de nova produção
        with st.form("form_producao"):
            st.text_input("Lote", value=lote_gerado, disabled=True)
            produto_opcoes = [p["nome"] for p in produtos] if produtos else ["-"]
            produto_nome = st.selectbox("Produto", produto_opcoes)
            funcionario_opcoes = [f"{f['nome']} ({f['funcao']})" for f in funcionarios] if funcionarios else ["-"]
            funcionario_nome = st.selectbox("Funcionário", funcionario_opcoes)
            quantidade = st.number_input("Quantidade", min_value=1, step=1)
            status = st.selectbox("Status Inicial", status_etapas[:-1])
            data = st.date_input("Data", value=datetime.today())
            submit = st.form_submit_button("Cadastrar Produção")
            if submit:
                # Validação dos campos do formulário
                if produto_nome and funcionario_nome and quantidade > 0:
                    nova = {
                        "lote": lote_gerado,
                        "produto_nome": produto_nome,
                        "funcionario_nome": funcionario_nome,
                        "quantidade": quantidade,
                        "status": status,
                        "data": str(data)
                    }
                    producoes.append(nova)
                    salvar_dados(ARQ_PRODUCOES, producoes)
                    st.success("Produção cadastrada!")
                    st.rerun()
                else:
                    st.error("Preencha todos os campos.")
    # --- Abas por etapa ---
    for idx, etapa_nome in enumerate(status_etapas):
        with aba[idx+1]:
            st.markdown(f"<h3 style='color:#1976d2;margin-bottom:12px;'>{etapa_icones.get(etapa_nome, '')} {etapa_nome} <span style='font-size:0.8em;color:#888'>({counts[etapa_nome]})</span></h3>", unsafe_allow_html=True)
            lista = [p for p in producoes if p["status"] == etapa_nome]
            if not lista:
                st.info(f"Nenhuma produção em {etapa_nome}.")
            for i, p in enumerate(lista):
                cor_card = etapa_cores.get(etapa_nome, "#f8f9fa")
                prox_idx = status_etapas.index(etapa_nome) + 1 if etapa_nome != "Concluído" else None
                prox_status = status_etapas[prox_idx] if prox_idx and prox_idx < len(status_etapas) else None
                with st.container():
                    card_html = f"""
                        <div style='background:{cor_card};border-radius:14px;padding:18px 24px;margin-bottom:18px;box-shadow:0 2px 12px #0001;display:flex;align-items:center;justify-content:space-between;'>
                            <div style='flex:1;min-width:220px;'>
                                <div style='font-size:1.25em;font-weight:600;color:#222;margin-bottom:2px;'>{etapa_icones.get(etapa_nome, '')} {p['produto_nome']}</div>
                                <div style='color:#555;font-size:1em;margin-bottom:2px;'><b>Lote:</b> {p['lote']}</div>
                                <div style='color:#555;font-size:1em;margin-bottom:2px;'><b>Funcionário:</b> {p['funcionario_nome']}</div>
                                <div style='color:#555;font-size:1em;margin-bottom:2px;'><b>Qtd:</b> {p['quantidade']} &nbsp; <b>Data:</b> {p['data']}</div>
                            </div>
                            <div style='min-width:220px;text-align:right;'>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                    move_key = f"move_{etapa_nome}_{i}"
                    move_state_key = f"move_state_{etapa_nome}_{i}"
                    confirm_key = f"confirma_{etapa_nome}_{i}"
                    select_key = f"func_{etapa_nome}_{i}"
                    if etapa_nome != "Concluído" and prox_status:
                        if move_state_key not in st.session_state:
                            st.session_state[move_state_key] = False
                        if prox_status == "Concluído":
                            if st.button(f"Mover para {prox_status}", key=move_key):
                                idx = producoes.index(p)
                                producoes[idx]["status"] = prox_status
                                salvar_dados(ARQ_PRODUCOES, producoes)
                                st.success(f"Produção movida para {prox_status}!")
                                st.session_state[move_state_key] = False
                                st.rerun()
                        else:
                            if st.button(f"Mover para {prox_status}", key=move_key):
                                st.session_state[move_state_key] = True
                            if st.session_state[move_state_key]:
                                novo_func = p["funcionario_nome"]
                                funcao_prox = prox_status[:-3] if prox_status.endswith('ndo') else prox_status
                                funcao_map = {
                                    "Cortando": "Cortador",
                                    "Costurando": "Costureira",
                                    "Revisando e Embalando": "Revisor"
                                }
                                funcao_filtrar = funcao_map.get(prox_status, None)
                                if funcao_filtrar:
                                    funcionarios_filtrados = [f for f in funcionarios if f["funcao"].lower() == funcao_filtrar.lower()]
                                else:
                                    funcionarios_filtrados = funcionarios
                                funcionario_opcoes = [f["nome"] + " (" + f["funcao"] + ")" for f in funcionarios_filtrados]
                                novo_func = st.selectbox(
                                    f"Selecione o funcionário para {prox_status}",
                                    funcionario_opcoes,
                                    key=select_key
                                )
                                if st.button(f"Confirmar", key=confirm_key):
                                    idx = producoes.index(p)
                                    producoes[idx]["status"] = prox_status
                                    producoes[idx]["funcionario_nome"] = novo_func
                                    salvar_dados(ARQ_PRODUCOES, producoes)
                                    st.success(f"Produção movida para {prox_status}!")
                                    st.session_state[move_state_key] = False
                                    st.rerun()
                    st.markdown("</div></div>", unsafe_allow_html=True)
