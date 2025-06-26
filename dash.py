import streamlit as st
import pandas as pd
import os
from PIL import Image
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard Premier League", layout="wide")

# Logo da Premier League
image_path = os.path.join(os.path.dirname(__file__), "premier_league_logo.jpg")
if os.path.exists(image_path):
    logo = Image.open(image_path)
    st.image(logo, width=100)

st.title("📊 Análise de Jogadores da Premier League 2024/25")

# Carregar dados com cache
@st.cache_data
def load_data(): 
    df = pd.read_csv("epl_player_stats_24_25.csv", index_col=False)
   
    df.columns = df.columns.str.encode('utf-8').str.decode('utf-8')
    df.columns = df.columns.str.strip().str.replace('\n', '').str.replace('\xa0', ' ', regex=False)
    return df

# Carrega dados na sessão
if "data" not in st.session_state:
    st.session_state["data"] = load_data()

df = st.session_state["data"]

# Verifica se as colunas necessárias existem
colunas_esperadas = ["Player Name", "Club", "Minutes", "Goals"]
colunas_faltando = [col for col in colunas_esperadas if col not in df.columns]

if colunas_faltando:
    st.warning(f"⚠️ As seguintes colunas estão faltando: {colunas_faltando}")
    st.stop()

# Seletor de clube
clubes = df["Club"].dropna().unique()
clube_selecionado = st.selectbox("Selecione o clube:", sorted(clubes))

# Filtra os jogadores do clube selecionado
df_clube = df[df["Club"] == clube_selecionado]

# Top 5 por minutos jogados
top_minutos = df_clube.sort_values(by="Minutes", ascending=False).head(5)

# Top 5 por gols marcados
top_gols = df_clube.sort_values(by="Goals", ascending=False).head(5)

# Exibe os dois rankings lado a lado
col1, col2 = st.columns(2)

with col1:
    st.subheader("⏱️ Top 5 - Jogadores com Mais Minutos")
    st.dataframe(top_minutos[["Player Name", "Minutes"]], use_container_width=True)
    fig_min = px.bar(top_minutos, x="Minutes", y="Player Name", orientation="h",
                     title="Top 5 - Minutos Jogados", color="Minutes", color_continuous_scale="Blues")
    st.plotly_chart(fig_min, use_container_width=True)

with col2:
    st.subheader("⚽ Top 5 - Jogadores com Mais Gols")
    st.dataframe(top_gols[["Player Name", "Goals"]], use_container_width=True)
    fig_gols = px.bar(top_gols, x="Goals", y="Player Name", orientation="h",
                      title="Top 5 - Gols Marcados", color="Goals", color_continuous_scale="Reds")
    st.plotly_chart(fig_gols, use_container_width=True)

# Gráfico geral do clube
st.subheader(f"📈 Desempenho Geral - {clube_selecionado}")
fig_geral = px.scatter(df_clube, x="Minutes", y="Goals", size="Goals", color="Player Name",
                       hover_name="Player Name", title="Minutos vs Gols", height=500)
st.plotly_chart(fig_geral, use_container_width=True)