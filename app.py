import streamlit as st
import pandas as pd
import plotly.express as px
from services.cotacao_service import CotacaoService

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
    
    .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_service():
    return CotacaoService()

service = get_service()

with st.sidebar:
    st.markdown("# 🏎️ Minerva Motors")
    st.markdown("---")
    st.markdown("### ⚙️ Filtros de Pesquisa")
    
    marcas_disponiveis = service.listar_marcas()
    marca = st.selectbox("Marca", marcas_disponiveis)
    
    modelos_disponiveis = service.listar_modelos(marca)
    modelo = st.selectbox("Modelo", modelos_disponiveis)
    
    ano = st.selectbox("Ano Modelo", [2026, 2025, 2024, 2023])
    
    st.markdown(" ") 
    buscar = st.button("🔍 BUSCAR OFERTAS")

if buscar:
    df_ofertas = service.buscar_ofertas(marca, modelo, ano)
    
    service.registrar_log({
        "marca": marca, 
        "modelo": modelo, 
        "ano": ano,
        "origem": "streamlit_ui"
    })

    if not df_ofertas.empty:
        kpis = service.calcular_kpis(df_ofertas)
        
        st.markdown(f"""## Resultados para: <span style='color:#FF4B4B'>{marca} {modelo} ({ano})</span>""", unsafe_allow_html=True)
        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)
        
        def kpi_card(title, value, subtext, color="#FF4B4B"):
            return f"""
            <div class="kpi-card" style="border-left: 5px solid {color}">
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-delta">{subtext}</div>
            </div>
            """

        with col1: st.markdown(kpi_card("Preço Médio", f"R$ {kpis['media']:,.2f}", "Calculado hoje", "#3498db"), unsafe_allow_html=True)
        with col2: st.markdown(kpi_card("Menor Oferta", f"R$ {kpis['min']:,.2f}", kpis['loja_mais_barata'], "#2ecc71"), unsafe_allow_html=True)
        with col3: st.markdown(kpi_card("Maior Oferta", f"R$ {kpis['max']:,.2f}", kpis['loja_mais_cara'], "#e74c3c"), unsafe_allow_html=True)
        with col4: st.markdown(kpi_card("Total Ofertas", str(kpis['total_ofertas']), kpis['regiao_predominante'], "#f1c40f"), unsafe_allow_html=True)

        st.markdown(" ")

        col_graf, col_tab = st.columns([2, 1])

        with col_graf:
            st.markdown("#### 📈 Histórico de Preços (Tendência)")
            df_hist = service.obter_historico_precos(modelo)
            
            if not df_hist.empty:
                fig = px.area(df_hist, x='Mês', y=['Preço Mínimo', 'Preço Médio', 'Preço Máximo'],
                              color_discrete_sequence=['#2ecc71', '#3498db', '#e74c3c'])
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_title="", hovermode="x unified")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Dados históricos insuficientes para gerar gráfico.")

        with col_tab:
            st.markdown("#### 📋 Detalhes das Ofertas")
            # Tabela Real
            st.dataframe(
                df_ofertas[["Loja", "Região", "Preço", "Opcionais"]].style.format({"Preço": "R$ {:.2f}"}),
                use_container_width=True,
                height=400,
                hide_index=True
            )
            
    else:
        st.warning(f"Nenhuma oferta encontrada para {marca} {modelo} no ano {ano}.")
        st.info("Dica: Tente mudar o ano ou verifique se o modelo possui cotações cadastradas.")

else:
    st.info("👈 Utilize os filtros laterais para iniciar a cotação.")
    st.markdown("---")
    st.caption("© 2026 Minerva Motors - Sistema Conectado ao PostgreSQL")