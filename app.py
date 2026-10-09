import re
import os
from datetime import datetime, timedelta

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


@st.cache_resource
def conectar_sheets():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes,
    )
    client = gspread.authorize(creds)
    return client.open("Aura — Registro de Propostas")


def registrar_proposta(dados: dict):
    try:
        aba = conectar_sheets().sheet1
        cabecalho = [
            "Data", "Nº Proposta", "Consultor", "Cliente", "Nº Processo",
            "Tribunal", "Natureza", "Valor de Face", "Valor Proposto",
            "Prazo Pagamento", "E-mail Consultor",
        ]
        cabecalho_atual = aba.row_values(1)
        if not cabecalho_atual:
            aba.append_row(cabecalho)
        elif "Nº Processo" not in cabecalho_atual:
            aba.insert_cols([["Nº Processo"]], col=5)

        nova_linha = [
            dados["data"], dados["numeroProposta"], dados["consultor"],
            dados["nomeCliente"], dados["numeroProcesso"], dados["tribunal"],
            dados["natureza"], dados["valorFace"], dados["valorProposto"],
            dados["prazoPagamento"], dados["email"],
        ]
        numeros_propostas = aba.col_values(2)
        if dados["numeroProposta"] in numeros_propostas:
            linha = numeros_propostas.index(dados["numeroProposta"]) + 1
            aba.update(range_name=f"A{linha}:K{linha}", values=[nova_linha])
            return "atualizada"
        aba.append_row(nova_linha)
        return "criada"
    except Exception:
        st.warning("⚠️ Proposta gerada, mas não foi possível registrar na planilha.")
        return False


st.set_page_config(
    page_title="Aura Capital — Gerador de Propostas",
    page_icon="📄",
    layout="centered",
)

CONSULTORES = {
    "Marcel Álvaro Mano de Incrocci": {
        "email": "marcel.incrocci@auracapitalsec.com.br",
        "telefone_consultor": "",
        "cargo": "Consultor Comercial",
    },
    "Igor Nolasco Diniz": {
        "email": "igor.diniz@auracapitalsec.com.br",
        "telefone_consultor": "",
        "cargo": "Consultor Comercial",
    },
    "Wander Moreira Alves": {
        "email": "wander.alves@auracapitalsec.com.br",
        "telefone_consultor": "",
        "cargo": "Head Comercial",
    },
    "Rafael da Silva Campos": {
        "email": "rafael.campos@auracapitalsec.com.br",
        "telefone_consultor": "",
        "cargo": "Supervisor Comercial",
    },
}

TRIBUNAIS = [
    "TJSP", "TJRJ", "TJMG", "TJRS", "TJPR", "TJSC", "TJBA",
    "TJGO", "TJMT", "TJMS", "TJPA", "TJAM", "TJCE", "TJPE", "TJDF",
    "TRF1", "TRF2", "TRF3", "TRF4", "TRF5", "TRF6",
    "STJ", "STF", "TNU",
]

NATUREZAS = [
    "Comum Não Tributável", "Comum Tributável",
    "Alimentar Não Tributável", "Alimentar Tributável",
    "Previdenciário", "Tributário",
]

st.markdown(
    """
<style>
    .main { background-color: #f8f7fc; }
    .block-container { padding-top: 2rem; max-width: 780px; }
    h1 { color: #252958; font-size: 1.6rem; }
    h3 { color: #3f52a0; font-size: 1rem; margin-top: 1.5rem; }
    .stButton > button {
        background-color: #252958; color: white; border: none;
        padding: 0.6rem 2rem; font-size: 1rem; font-weight: 600;
        border-radius: 6px; width: 100%;
    }
    .stButton > button:hover { background-color: #3f52a0; }
    .stDownloadButton > button {
        background-color: #c9a832; color: #252958; border: none;
        padding: 0.6rem 2rem; font-size: 1rem; font-weight: 700;
        border-radius: 6px; width: 100%;
    }
    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label {
        font-weight: 600; color: #252958;
    }
</style>
""",
    unsafe_allow_html=True,
)


def formatar_brl(valor):
    if not valor:
        return ""
    texto = str(valor).strip().replace("R$", "").replace(" ", "")
    try:
        if "," in texto:
            texto = texto.replace(".", "").replace(",", ".")
            numero = float(texto)
        elif "." in texto and len(texto.split(".")[-1]) == 2:
            numero = float(texto)
        else:
            texto = texto.replace(".", "")
            numero = float(texto)
        formatado = f"{numero:,.2f}"
        formatado = formatado.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {formatado}"
    except ValueError:
        return valor


def formatar_campo_moeda(chave):
    st.session_state[chave] = formatar_brl(st.session_state.get(chave, ""))


def gerar_html(cliente: dict) -> str:
    template_path = os.path.join(os.path.dirname(__file__), "template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    gm_logo_path = os.path.join(os.path.dirname(__file__), "gm_logo.b64")
    if os.path.exists(gm_logo_path):
        with open(gm_logo_path, "r", encoding="utf-8") as f:
            gm_logo_b64 = "".join(f.read().split())

        branding_css = """
    /* BRANDING INSTITUCIONAL AURA + GALERA MARI */
    .header img.logo {
      left: 36px;
      top: 37%;
      height: 40px;
    }
    .header img.gm-logo {
      position: absolute;
      left: 255px;
      top: 37%;
      transform: translateY(-50%);
      height: 37px;
      width: auto;
      max-width: 150px;
      object-fit: contain;
      background: transparent !important;
      padding: 0 !important;
      border-radius: 0 !important;
      filter: brightness(0) invert(1);
    }
    .header .brand-divider {
      position: absolute;
      left: 232px;
      top: 15px;
      height: 38px;
      width: 1px;
      background: rgba(255,255,255,.35);
    }
    .header .institutional-signature {
      position: absolute;
      left: 36px;
      bottom: 9px;
      font-size: 7px;
      font-weight: 500;
      color: #b8bbd5;
      letter-spacing: .45px;
      white-space: nowrap;
    }
"""
        html = html.replace("</style>", branding_css + "  </style>", 1)
        branding_html = (
            '<span class="brand-divider"></span>'
            f'<img class="gm-logo" src="data:image/png;base64,{gm_logo_b64}" '
            'alt="Galera Mari Advogados - 40 anos">'
            '<div class="institutional-signature">'
            'Aura Capital Securitizadora S.A. &nbsp;·&nbsp; '
            'Braço financeiro do ecossistema Galera Mari'
            '</div>'
        )
        html = re.sub(
            r'(<img class="logo"[^>]*>)',
            lambda m: m.group(1) + branding_html,
            html,
            count=1,
        )

    for chave, valor in cliente.items():
        html = re.sub(r"\{\{\s*" + chave + r"\s*\}\}", str(valor), html)

    pendentes = re.findall(r"\{\{.*?\}\}", html)
    if pendentes:
        st.warning(f"⚠️ Campos não preenchidos no template: {pendentes}")
    return html


st.markdown("## 📄 Gerador de Propostas")
st.markdown("**Aura Capital Securitizadora** · Antecipação de Crédito Judicial")
st.divider()

st.markdown("### 👤 Consultor Responsável")
nome_consultor = st.selectbox(
    "Selecione o consultor",
    options=list(CONSULTORES.keys()),
    index=0,
)
dados_consultor = CONSULTORES[nome_consultor]
st.caption(f"{dados_consultor['cargo']} · {dados_consultor['email']}")

st.divider()
st.markdown("### 🧾 Dados do Cliente")
col1, col2 = st.columns(2)
with col1:
    nome_cliente = st.text_input("Nome completo do credor", placeholder="Ex: MARIA DA SILVA SANTOS")
with col2:
    telefone = st.text_input("WhatsApp (com DDD e código do país)", placeholder="5565999999999")

numero_processo = st.text_input("Número do Processo", placeholder="0012345-67.2023.8.26.0100")
col3, col4 = st.columns(2)
with col3:
    tribunal = st.selectbox("Tribunal", options=TRIBUNAIS, index=0)
with col4:
    natureza = st.selectbox("Natureza", options=NATUREZAS, index=0)

st.divider()
st.markdown("### 💰 Dados da Operação")
col5, col6 = st.columns(2)
with col5:
    valor_face = st.text_input(
        "Valor de Face do Precatório", placeholder="Ex: 500000",
        key="valor_face", on_change=formatar_campo_moeda, args=("valor_face",),
    )
with col6:
    valor_proposto = st.text_input(
        "Valor Proposto (oferta)", placeholder="Ex: 150000",
        key="valor_proposto", on_change=formatar_campo_moeda, args=("valor_proposto",),
    )

col7, col8 = st.columns(2)
with col7:
    prazo_pagamento = st.selectbox(
        "Prazo de Pagamento",
        options=["5 dias úteis", "7 dias úteis", "10 dias úteis", "15 dias úteis"],
    )
with col8:
    numero_proposta = st.text_input(
        "Número da Proposta",
        value=(f"2026-{datetime.now().month:02d}-"
               f"{datetime.now().day:02d}{datetime.now().hour:02d}"
               f"{datetime.now().minute:02d}"),
    )

st.divider()

if st.button("🚀 Gerar Proposta"):
    campos_obrigatorios = {
        "Nome do credor": nome_cliente,
        "Número do processo": numero_processo,
        "Valor de face": valor_face,
        "Valor proposto": valor_proposto,
        "Telefone": telefone,
    }
    campos_vazios = [k for k, v in campos_obrigatorios.items() if not str(v).strip()]
    if campos_vazios:
        st.error(f"Preencha os campos obrigatórios: {', '.join(campos_vazios)}")
    else:
        with st.spinner("Gerando proposta..."):
            hoje = datetime.now()
            validade = hoje + timedelta(days=7)
            meses = [
                "janeiro", "fevereiro", "março", "abril", "maio", "junho",
                "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
            ]
            partes = nome_consultor.split()
            iniciais = (partes[0][0] + partes[-1][0]).upper() if len(partes) >= 2 else partes[0][:2].upper()
            cliente = {
                "nomeCliente": nome_cliente.upper(),
                "telefone": telefone,
                "numeroProposta": numero_proposta,
                "numeroProcesso": numero_processo,
                "valorFace": valor_face,
                "tribunal": tribunal,
                "natureza": natureza,
                "valorProposto": valor_proposto,
                "prazoPagamento": prazo_pagamento,
                "consultor": nome_consultor,
                "email": dados_consultor["email"],
                "cargo": dados_consultor["cargo"],
                "iniciais": iniciais,
                "data": f"{hoje.day} de {meses[hoje.month - 1]} de {hoje.year}",
                "validade": f"{validade.day} de {meses[validade.month - 1]} de {validade.year}",
            }
            try:
                html_content = gerar_html(cliente)
                nome_arquivo = f"Proposta_{nome_cliente.replace(' ', '_')}_{numero_proposta}.html"
                output_dir = os.path.join(os.path.dirname(__file__), "output")
                os.makedirs(output_dir, exist_ok=True)
                caminho_html = os.path.join(output_dir, nome_arquivo)
                with open(caminho_html, "w", encoding="utf-8") as f:
                    f.write(html_content)

                status_registro = registrar_proposta(cliente)
                if status_registro == "atualizada":
                    st.success("✅ Proposta atualizada com sucesso! O registro existente foi substituído na planilha.")
                elif status_registro == "criada":
                    st.success("✅ Proposta gerada e registrada com sucesso!")
                else:
                    st.success("✅ Proposta gerada com sucesso!")

                st.download_button(
                    label="⬇️ Baixar Proposta (HTML)",
                    data=html_content.encode("utf-8"),
                    file_name=nome_arquivo,
                    mime="text/html",
                )
                st.info(
                    "**Como salvar como PDF:**\n"
                    "1. Clique em '⬇️ Baixar Proposta (HTML)' acima\n"
                    "2. Abra o arquivo no Chrome\n"
                    "3. Pressione **Cmd+P** → Destino: **Salvar como PDF** → Salvar"
                )

                log_path = os.path.join(os.path.dirname(__file__), "log.txt")
                with open(log_path, "a", encoding="utf-8") as log:
                    log.write(
                        f"{datetime.now().strftime('%Y-%m-%d %H:%M')} | "
                        f"{nome_consultor} | {nome_cliente} | {numero_proposta} | {valor_proposto}\n"
                    )
            except Exception as e:
                st.error(f"Erro ao gerar proposta: {e}")

st.divider()
st.caption("Aura Capital Securitizadora S.A. · atendimento@auracapitalsec.com.br")