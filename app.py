import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Minerva Motors | Cotação Inteligente",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
    }

    /* Cards de KPI */
    .kpi-card {
        background-color: #262730;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        border-left: 5px solid #FF4B4B;
        text-align: center;
    }
    .kpi-title { font-size: 14px; color: #b0b0b0; text-transform: uppercase; margin-bottom: 5px; }
    .kpi-value { font-size: 28px; font-weight: bold; color: #ffffff; }
    .kpi-delta { font-size: 12px; color: #00CC96; }

    /* Botão Principal */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #FF4B4B 0%, #FF2B2B 100%);
        color: white;
        border: none;
        padding: 15px;
        font-weight: bold;
        text-transform: uppercase;
        border-radius: 8px;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
    }
    
    /* Remove padding do topo */
    .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

def get_historico_fake():
    dates = pd.date_range(start="2025-09-01", periods=6, freq='ME')
    data = {
        'Mês': dates,
        'Preço Médio': [44500, 44800, 44200, 45100, 45500, 45200],
        'Preço Mínimo': [43000, 43500, 43000, 44000, 44200, 44000],
        'Preço Máximo': [46000, 46500, 45500, 46800, 47000, 46500]
    }
    return pd.DataFrame(data)

df_historico = get_historico_fake()

with st.sidebar:
    st.markdown("# 🏎️ Minerva Motors")
    st.markdown("---")
    st.markdown("### ⚙️ Filtros de Pesquisa")
    
    marca = st.selectbox("Marca", ["Fiat", "Honda", "Toyota", "VW"])
    modelos_dict = {"Fiat": ["Palio", "Mobi"], "Honda": ["Civic", "Fit"], "Toyota": ["Corolla"], "VW": ["Gol"]}
    modelo = st.selectbox("Modelo", modelos_dict.get(marca, ["Selecione"]))
    ano = st.selectbox("Ano Modelo", [2026, 2025, 2024])
    
    st.markdown(" ") 
    st.markdown(" ") 
    
    buscar = st.button("🔍 BUSCAR OFERTAS")
    
    if buscar:
        st.session_state['buscou'] = True
    if 'buscou' not in st.session_state:
        st.session_state['buscou'] = True 

if st.session_state['buscou']:
    st.markdown(f"""## Resultados para: <span style='color:#FF4B4B'>{marca} {modelo} ({ano})</span>""", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    
    def kpi_card(title, value, delta, color="#FF4B4B"):
        return f"""
        <div class="kpi-card" style="border-left: 5px solid {color}">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-delta">{delta}</div>
        </div>
        """

    with col1: st.markdown(kpi_card("Preço Médio", "R$ 45.200", "▲ 1.2%", "#3498db"), unsafe_allow_html=True)
    with col2: st.markdown(kpi_card("Menor Oferta", "R$ 44.000", "Autos Russas", "#2ecc71"), unsafe_allow_html=True)
    with col3: st.markdown(kpi_card("Maior Oferta", "R$ 46.500", "Cariri Motors", "#e74c3c"), unsafe_allow_html=True)
    with col4: st.markdown(kpi_card("Disponibilidade", "12 Lojas", "Ceará", "#f1c40f"), unsafe_allow_html=True)

    st.markdown(" ")

    col_graf, col_tab = st.columns([2, 1])

    with col_graf:
        st.markdown("#### 📈 Evolução de Preços")
        fig = px.area(df_historico, x='Mês', y=['Preço Mínimo', 'Preço Médio', 'Preço Máximo'],
                      color_discrete_sequence=['#2ecc71', '#3498db', '#e74c3c'])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            legend_title="", margin=dict(l=0, r=0, t=0, b=0), hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_tab:
        st.markdown("#### 📋 Top Ofertas")
        df_ofertas = pd.DataFrame({
            "Loja": ["Autos Russas", "Fortal Veic", "Sobral Car", "Cariri Motors", "Iguatu Auto"],
            "Cidade": ["Russas", "Fortaleza", "Sobral", "Juazeiro", "Iguatu"],
            "Preço": [44000, 44500, 44800, 46500, 45000]
        })
        
        st.dataframe(
            df_ofertas.style.background_gradient(subset=['Preço'], cmap="RdYlGn_r", vmin=43000, vmax=47000)
                              .format({"Preço": "R$ {:.2f}"}),
            use_container_width=True,
            height=300,
            hide_index=True
        )

    st.markdown("---")
    st.caption("© 2026 Minerva Motors - Sistema de Cotação")

else:
    st.info("Utilize os filtros laterais para iniciar.")