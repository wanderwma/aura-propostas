import re
import os
import base64
from datetime import datetime, timedelta
import streamlit as st

# ══════════════════════════════════════════════
# CONFIGURAÇÃO DA PÁGINA
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="Aura Capital — Gerador de Propostas",
    page_icon="📄",
    layout="centered"
)

# ══════════════════════════════════════════════
# CSS PERSONALIZADO
# ══════════════════════════════════════════════
st.markdown("""
<style>
    .main { background-color: #f8f7fc; }
    .block-container { padding-top: 2rem; max-width: 780px; }
    h1 { color: #252958; font-size: 1.6rem; }
    h3 { color: #3f52a0; font-size: 1rem; margin-top: 1.5rem; }
    .stButton > button {
        background-color: #252958;
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 6px;
        width: 100%;
    }
    .stButton > button:hover { background-color: #3f52a0; }
    .stDownloadButton > button {
        background-color: #c9a832;
        color: #252958;
        border: none;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 700;
        border-radius: 6px;
        width: 100%;
    }
    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label {
        font-weight: 600;
        color: #252958;
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# CONSULTORES CADASTRADOS
# ══════════════════════════════════════════════
CONSULTORES = {
    "Marcel Álvaro Mano de Incrocci": {
        "email": "marcel.incrocci@auracapitalsec.com.br",
        "telefone_consultor": "",
        "cargo": "Consultor Comercial"
    },
    "Breno Borges de Figueiredo": {
        "email": "breno.figueiredo@auracapitalsec.com.br",
        "telefone_consultor": "",
        "cargo": "Consultor Comercial"
    },
    "Wander Moreira Alves": {
        "email": "wander.alves@auracapitalsec.com.br",
        "telefone_consultor": "",
        "cargo": "Head Comercial"
    },
}

TRIBUNAIS = [
    "TJSP", "TJRJ", "TJMG", "TJRS", "TJPR", "TJSC", "TJBA",
    "TJGO", "TJMT", "TJMS", "TJPA", "TJAM", "TJCE", "TJPE",
    "TRF1", "TRF2", "TRF3", "TRF4", "TRF5",
    "STJ", "STF", "TNU"
]

NATUREZAS = [
    "Comum Não Tributável",
    "Comum Tributável",
    "Alimentar Não Tributável",
    "Alimentar Tributável",
    "Previdenciário",
    "Tributário",
]

# ══════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════
st.markdown("## 📄 Gerador de Propostas")
st.markdown("**Aura Capital Securitizadora** · Antecipação de Crédito Judicial")
st.divider()

# ══════════════════════════════════════════════
# FORMULÁRIO
# ══════════════════════════════════════════════

# — Consultor —
st.markdown("### 👤 Consultor Responsável")
nome_consultor = st.selectbox(
    "Selecione o consultor",
    options=list(CONSULTORES.keys()),
    index=0
)
dados_consultor = CONSULTORES[nome_consultor]
st.caption(f"📧 {dados_consultor['email']}")

st.divider()

# — Dados do Cliente —
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

# — Dados da Operação —
st.markdown("### 💰 Dados da Operação")

col5, col6 = st.columns(2)
with col5:
    valor_face = st.text_input("Valor de Face do Precatório", placeholder="R$1.000.000,00")
with col6:
    valor_proposto = st.text_input("Valor Proposto (oferta)", placeholder="R$150.000,00")

col7, col8 = st.columns(2)
with col7:
    prazo_pagamento = st.selectbox(
        "Prazo de Pagamento",
        options=["5 dias úteis", "7 dias úteis", "10 dias úteis", "15 dias úteis"]
    )
with col8:
    numero_proposta = st.text_input(
        "Número da Proposta",
        value=f"2026-{datetime.now().month:02d}-{datetime.now().day:02d}{datetime.now().hour:02d}{datetime.now().minute:02d}"
    )

st.divider()

# ══════════════════════════════════════════════
# GERAÇÃO DO HTML (sem dependências externas)
# ══════════════════════════════════════════════
def gerar_html(cliente: dict) -> str:
    template_path = os.path.join(os.path.dirname(__file__), "template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    for chave, valor in cliente.items():
        html = re.sub(r"\{\{\s*" + chave + r"\s*\}\}", str(valor), html)

    pendentes = re.findall(r"\{\{.*?\}\}", html)
    if pendentes:
        st.warning(f"⚠️ Campos não preenchidos no template: {pendentes}")

    return html


if st.button("🚀 Gerar Proposta"):

    campos_obrigatorios = {
        "Nome do credor": nome_cliente,
        "Número do processo": numero_processo,
        "Valor de face": valor_face,
        "Valor proposto": valor_proposto,
        "Telefone": telefone,
    }
    campos_vazios = [k for k, v in campos_obrigatorios.items() if not v.strip()]

    if campos_vazios:
        st.error(f"Preencha os campos obrigatórios: {', '.join(campos_vazios)}")
    else:
        with st.spinner("Gerando proposta..."):

            hoje = datetime.now()
            validade = hoje + timedelta(days=7)
            meses = [
                "janeiro","fevereiro","março","abril","maio","junho",
                "julho","agosto","setembro","outubro","novembro","dezembro"
            ]
            partes = nome_consultor.split()
            iniciais = (partes[0][0] + partes[-1][0]).upper() if len(partes) >= 2 else partes[0][:2].upper()

            cliente = {
                "nomeCliente":    nome_cliente.upper(),
                "telefone":       telefone,
                "numeroProposta": numero_proposta,
                "numeroProcesso": numero_processo,
                "valorFace":      valor_face,
                "tribunal":       tribunal,
                "natureza":       natureza,
                "valorProposto":  valor_proposto,
                "prazoPagamento": prazo_pagamento,
                "consultor":      nome_consultor,
                "email":          dados_consultor["email"],
                "cargo":          dados_consultor["cargo"],
                "iniciais":       iniciais,
                "data":           f"{hoje.day} de {meses[hoje.month-1]} de {hoje.year}",
                "validade":       f"{validade.day} de {meses[validade.month-1]} de {validade.year}",
            }

            try:
                html_content = gerar_html(cliente)
                nome_arquivo = f"Proposta_{nome_cliente.replace(' ', '_')}_{numero_proposta}.html"

                # Salva o HTML na pasta Aura-Propostas/output/
                output_dir = os.path.join(os.path.dirname(__file__), "output")
                os.makedirs(output_dir, exist_ok=True)
                caminho_html = os.path.join(output_dir, nome_arquivo)
                with open(caminho_html, "w", encoding="utf-8") as f:
                    f.write(html_content)

                st.success("✅ Proposta gerada com sucesso!")

                # Botão de download do HTML
                html_bytes = html_content.encode("utf-8")
                st.download_button(
                    label="⬇️ Baixar Proposta (HTML)",
                    data=html_bytes,
                    file_name=nome_arquivo,
                    mime="text/html"
                )

                st.info(
                    "**Como salvar como PDF:**\n"
                    "1. Clique em '⬇️ Baixar Proposta (HTML)' acima\n"
                    "2. Abra o arquivo no Chrome\n"
                    "3. Pressione **Cmd+P** → Destino: **Salvar como PDF** → Salvar"
                )

                # Log local
                log_path = os.path.join(os.path.dirname(__file__), "log.txt")
                with open(log_path, "a", encoding="utf-8") as log:
                    log.write(
                        f"{datetime.now().strftime('%Y-%m-%d %H:%M')} | "
                        f"{nome_consultor} | {nome_cliente} | {numero_proposta} | {valor_proposto}\n"
                    )

            except Exception as e:
                st.error(f"Erro ao gerar proposta: {e}")

# ══════════════════════════════════════════════
# RODAPÉ
# ══════════════════════════════════════════════
st.divider()
st.caption("Aura Capital Securitizadora S.A. · atendimento@auracapitalsec.com.br")
