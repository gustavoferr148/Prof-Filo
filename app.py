pip install streamlit plotly pandas

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Configuração da página (Tema Escuro nativo do Streamlit ajuda no visual)
st.set_page_config(page_title="Simulador de Pontuação", layout="centered")

st.title("Calculadora Interativa de Renda")
st.write("Arraste o slider ou digite um valor de renda para ver a pontuação calculada em tempo real.")

# 2. Entrada de Dados (Slider e Input Numérico integrados)
renda = st.slider(
    "Renda Líquida Per Capita (R$)", 
    min_value=0.0, 
    max_value=12000.0, 
    value=2818.55, 
    step=50.0
)

# 3. Lógica do Score e Regra de Negócio (Cap)
LIMITE_SUPERIOR = 5637.10

if renda <= LIMITE_SUPERIOR:
    # Fórmula: 5 - (coeficiente * renda)
    pontuacao = 5.0 - (5.0 / LIMITE_SUPERIOR) * renda
    zona = "Regular"
else:
    pontuacao = 0.0
    zona = "Zona de Outliers / Cap (0)"

# 4. Exibição dos Resultados (Cards informativos)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Renda Informada", value=f"R$ {renda:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
with col2:
    st.metric(label="Pontuação", value=f"{pontuacao:.2f}")
with col3:
    st.metric(label="Status da Zona", value=zona)

# 5. Construção do Gráfico Dinâmico (Plotly)
# Gerando os pontos da linha para o gráfico de fundo
x_curva = np.linspace(0, 12000, 500)
y_curva = np.where(x_curva <= LIMITE_SUPERIOR, 5.0 - (5.0 / LIMITE_SUPERIOR) * x_curva, 0.0)

fig = go.Figure()

# Linha da regra de pontuação
fig.add_trace(go.Scatter(
    x=x_curva, y=y_curva, 
    mode='lines', 
    name='Curva de Pontuação',
    line=dict(color='#636EFA', width=3)
))

# Ponto laranja dinâmico onde o cliente está mexendo
fig.add_trace(go.Scatter(
    x=[renda], y=[pontuacao], 
    mode='markers', 
    name='Posição Atual',
    marker=dict(color='#EF553B', size=12, line=dict(color='white', width=2))
))

# Ajustes de layout para combinar com a interface escura
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

# Renderiza o gráfico na tela
st.plotly_chart(fig, use_container_width=True)

streamlit run app.py
