import streamlit as st
import numpy as np
import plotly.graph_objects as go
import os

# 1. Configuração da página
# Usamos 'centered' para manter a largura fixa e profissional.
st.set_page_config(page_title="Simulador de Pontuação", layout="centered")

# --- TOPO DA PÁGINA ---

# Título Principal (Agora no topo, centralizado)
st.markdown("<h1 style='text-align: center;'>Calculadora Interativa de Renda</h1>", unsafe_allow_html=True)
st.write("---")

# --- LÓGICA DE SINCRONIZAÇÃO (BIDIRECIONAL PERFEITA) ---
# Inicializamos a memória de cada componente com o mesmo valor padrão
if 'valor_slider' not in st.session_state:
    st.session_state.valor_slider = 2818.55
if 'valor_caixa' not in st.session_state:
    st.session_state.valor_caixa = 2818.55

# Quando a barra se move, ela força a caixinha a receber o mesmo valor
def slider_mudou():
    st.session_state.valor_caixa = st.session_state.valor_slider

# Quando a caixinha é digitada, ela força a barra a ir para a mesma posição
def caixa_mudou():
    st.session_state.valor_slider = st.session_state.valor_caixa
# -----------------------------------------------------------

# 2. Entrada de Dados (Colunas lado a lado)
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

# A renda oficial para o cálculo usa o estado sincronizado
renda = st.session_state.valor_slider

# 3. Lógica do Score e Regra de Negócio (Cap)
LIMITE_SUPERIOR = 5637.10

if renda <= LIMITE_SUPERIOR:
    pontuacao = 5.0 - (5.0 / LIMITE_SUPERIOR) * renda
    zona = "Regular"
else:
    pontuacao = 0.0
    zona = "Zona de Outliers / Cap (0)"

# 4. Exibição dos Resultados (Cards informativos)
st.write("") # Adiciona um espacinho
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Renda Informada", value=f"R$ {renda:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
with col2:
    st.metric(label="Pontuação", value=f"{pontuacao:.2f}")
with col3:
    st.metric(label="Status da Zona", value=zona)

# 5. Construção do Gráfico Dinâmico (Plotly)
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

# --- NOVO RODAPÉ DE BRANDING (LOGO AMPLIADA E SOZINHA NO FINAL) ---
st.write("---") # Linha separadora discreta
# Centraliza a logo usando colunas com proporções ajustadas para uma imagem maior [1, 2, 1]
col_l1, col_l2, col_l3 = st.columns([1, 2, 1])

with col_l2:
    if os.path.exists("logo_jr.png"):
        # Exibe a logo (aumentamos a largura de 150 para 300)
        st.image("logo_jr.png", width=300)
    else:
        # Placeholder centralizado caso a imagem não exista
        st.markdown("<center>*(Logo JR Consultoria)*</center>", unsafe_allow_html=True)

# REMOVEMOS AQUI A LINHA QUE EXIBIA O TEXTO "Inteligência em Dados"
