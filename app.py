import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Configuração da página
st.set_page_config(page_title="Simulador de Pontuação", layout="centered")

st.title("Calculadora Interativa de Renda")
st.write("Arraste a barra ou digite o valor exato na caixinha para calcular a pontuação em tempo real.")

# --- LÓGICA DE SINCRONIZAÇÃO ENTRE SLIDER E CAIXA DE TEXTO ---
# Inicializa o valor padrão caso o app acabe de abrir
if 'renda' not in st.session_state:
    st.session_state.renda = 2818.55

# Funções que rodam quando o usuário mexe em um dos componentes
def atualiza_pelo_slider():
    st.session_state.renda = st.session_state.slider_input

def atualiza_pela_caixa():
    st.session_state.renda = st.session_state.caixa_input
# ------------------------------------------------------------

# 2. Entrada de Dados (Criando colunas para ficarem lado a lado)
col_slider, col_caixa = st.columns([3, 1])

with col_slider:
    st.slider(
        "Arraste para ajustar:", 
        min_value=0.0, 
        max_value=12000.0, 
        step=1.0,
        key="slider_input",
        value=st.session_state.renda,
        on_change=atualiza_pelo_slider
    )

with col_caixa:
    st.number_input(
        "Ou digite aqui:", 
        min_value=0.0, 
        max_value=12000.0, 
        step=1.0,
        key="caixa_input",
        value=st.session_state.renda,
        on_change=atualiza_pela_caixa
    )

# A variável 'renda' oficial do cálculo assume o valor sincronizado
renda = st.session_state.renda

# 3. Lógica do Score e Regra de Negócio (Cap)
LIMITE_SUPERIOR = 5637.10

if renda <= LIMITE_SUPERIOR:
    pontuacao = 5.0 - (5.0 / LIMITE_SUPERIOR) * renda
    zona = "Regular"
else:
    pontuacao = 0.0
    zona = "Zona de Outliers / Cap (0)"

# 4. Exibição dos Resultados (Cards)
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
