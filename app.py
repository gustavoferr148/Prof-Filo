import streamlit as st
import numpy as np
import plotly.graph_objects as go
import os

# 1. Configuração da página
st.set_page_config(page_title="Calculadora da Pontuação Pela Renda", layout="centered")

# --- SEÇÃO DE BRANDING (LOGO) ---
# Verifica se a imagem existe na pasta para não dar erro
if os.path.exists("logo_jr.png"):
    # Centraliza a logo usando colunas
    col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
    with col_l2:
        st.image("logo_jr.png", width=200)
else:
    # Caso você ainda não tenha subido a imagem, ele apenas pula
    st.write("*(Logo JR Consultoria)*") 
# --------------------------------

st.markdown("<h1 style='text-align: center;'>Calculadora da Pontuação Pela Renda</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Arrastar para ajustar ou escrever na caixa de texto a renda</p>", unsafe_allow_html=True)
st.write("---")

# --- LÓGICA DE SINCRONIZAÇÃO (BIDIRECIONAL) ---
if 'valor_slider' not in st.session_state:
    st.session_state.valor_slider = 2818.55
if 'valor_caixa' not in st.session_state:
    st.session_state.valor_caixa = 2818.55

def slider_mudou():
    st.session_state.valor_caixa = st.session_state.valor_slider

def caixa_mudou():
    st.session_state.valor_slider = st.session_state.valor_caixa

# 2. Entrada de Dados
col_slider, col_caixa = st.columns([3, 1])

with col_slider:
    st.slider(
        "Arraste para ajustar:", 
        min_value=0.0, 
        max_value=12000.0, 
        step=1.0,
        key="valor_slider",
        on_change=slider_mudou
    )

with col_caixa:
    st.number_input(
        "Ou digite aqui:", 
        min_value=0.0, 
        max_value=12000.0, 
        step=1.0,
        key="valor_caixa",
        on_change=caixa_mudou
    )

renda = st.session_state.valor_slider

# 3. Lógica do Score e Regra de Negócio (Cap)
LIMITE_SUPERIOR = 5637.10

if renda <= LIMITE_SUPERIOR:
    pontuacao = 5.0 - (5.0 / LIMITE_SUPERIOR) * renda
    zona = "Regular"
else:
    pontuacao = 0.0
    zona = "Zona de Outliers / Cap (0)"

# 4. Exibição dos Resultados (Cards)
st.write("")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Renda Informada", value=f"R$ {renda:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
with col2:
    st.metric(label="Pontuação", value=f"{pontuacao:.2f}")
with col3:
    st.metric(label="Status da Zona", value=zona)

# 5. Construção do Gráfico Dinâmico
x_curva = np.linspace(0, 12000, 500)
y_curva = np.where(x_curva <= LIMITE_SUPERIOR, 5.0 - (5.0 / LIMITE_SUPERIOR) * x_curva, 0.0)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_curva, y=y_curva, 
    mode='lines', 
    name='Curva de Pontuação',
    line=dict(color='#636EFA', width=3)
))

fig.add_trace(go.Scatter(
    x=[renda], y=[pontuacao], 
    mode='markers', 
    name='Posição Atual',
    marker=dict(color='#EF553B', size=12, line=dict(color='white', width=2))
))

fig.update_layout(
    xaxis_title="Renda Líquida Per Capita (R$)",
    yaxis_title="Pontuação",
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20),
    height=350
)

st.plotly_chart(fig, use_container_width=True)

# Rodapé discreto
st.markdown("<br><hr><center><small>JR Consultoria</small></center>", unsafe_allow_html=True)
