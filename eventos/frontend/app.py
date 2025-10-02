"""
Frontend Streamlit para EventRadar
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(
    page_title="EventRadar",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# URL da API
API_BASE_URL = "http://localhost:8000"

# CSS personalizado
st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .event-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


def fetch_events(filters=None):
    """Busca eventos da API"""
    try:
        url = f"{API_BASE_URL}/eventos/"
        params = filters or {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar eventos: {e}")
        return []


def fetch_cities():
    """Busca cidades disponíveis"""
    try:
        response = requests.get(f"{API_BASE_URL}/eventos/cidades/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return []


def fetch_event_types():
    """Busca tipos de eventos"""
    try:
        response = requests.get(f"{API_BASE_URL}/eventos/tipos/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return []


def main():
    # Header principal
    st.markdown('<h1 class="main-header">🎪 EventRadar</h1>', unsafe_allow_html=True)
    st.markdown("### Plataforma de Eventos com IA")

    # Sidebar com filtros
    st.sidebar.header("🔍 Filtros")

    # Filtros
    cidade = st.sidebar.selectbox("Cidade", ["Todas"] + fetch_cities(), index=0)

    tipo = st.sidebar.selectbox(
        "Tipo de Evento", ["Todos"] + fetch_event_types(), index=0
    )

    gratuito = st.sidebar.selectbox("Preço", ["Todos", "Gratuitos", "Pagos"], index=0)

    # Construir filtros
    filters = {}
    if cidade != "Todas":
        filters["cidade"] = cidade
    if tipo != "Todos":
        filters["tipo"] = tipo
    if gratuito == "Gratuitos":
        filters["gratuito"] = True
    elif gratuito == "Pagos":
        filters["gratuito"] = False

    # Buscar eventos
    eventos = fetch_events(filters)

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total de Eventos", len(eventos))

    with col2:
        eventos_gratuitos = len([e for e in eventos if e.get("gratuito", False)])
        st.metric("Eventos Gratuitos", eventos_gratuitos)

    with col3:
        eventos_proximos = len([e for e in eventos if e.get("data_inicio")])
        st.metric("Eventos Próximos", eventos_proximos)

    with col4:
        cidades_unicas = len(set(e.get("cidade", "") for e in eventos))
        st.metric("Cidades", cidades_unicas)

    # Gráficos
    if eventos:
        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de tipos de eventos
            tipos_count = {}
            for evento in eventos:
                tipo = evento.get("tipo", "outros")
                tipos_count[tipo] = tipos_count.get(tipo, 0) + 1

            if tipos_count:
                fig_tipos = px.pie(
                    values=list(tipos_count.values()),
                    names=list(tipos_count.keys()),
                    title="Distribuição por Tipo",
                )
                st.plotly_chart(fig_tipos, use_container_width=True)

        with col2:
            # Gráfico de eventos por cidade
            cidades_count = {}
            for evento in eventos:
                cidade = evento.get("cidade", "Outras")
                cidades_count[cidade] = cidades_count.get(cidade, 0) + 1

            if cidades_count:
                fig_cidades = px.bar(
                    x=list(cidades_count.keys()),
                    y=list(cidades_count.values()),
                    title="Eventos por Cidade",
                )
                st.plotly_chart(fig_cidades, use_container_width=True)

    # Lista de eventos
    st.header("📅 Eventos Encontrados")

    if not eventos:
        st.info("Nenhum evento encontrado com os filtros selecionados.")
        return

    # Paginação
    eventos_por_pagina = 10
    total_paginas = (len(eventos) - 1) // eventos_por_pagina + 1

    if total_paginas > 1:
        pagina = st.selectbox("Página", range(1, total_paginas + 1))
        inicio = (pagina - 1) * eventos_por_pagina
        fim = inicio + eventos_por_pagina
        eventos_pagina = eventos[inicio:fim]
    else:
        eventos_pagina = eventos

    # Exibir eventos
    for evento in eventos_pagina:
        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"### {evento.get('titulo', 'Sem título')}")

                # Informações básicas
                info_cols = st.columns(4)
                with info_cols[0]:
                    st.write(f"📍 {evento.get('local', 'Local não informado')}")
                with info_cols[1]:
                    st.write(f"🏙️ {evento.get('cidade', 'Cidade não informada')}")
                with info_cols[2]:
                    st.write(f"📅 {evento.get('data_inicio', 'Data não informada')}")
                with info_cols[3]:
                    if evento.get("gratuito", False):
                        st.write("💰 Gratuito")
                    else:
                        preco = evento.get("preco", 0)
                        st.write(f"💰 R$ {preco:.2f}")

                # Descrição
                if evento.get("descricao"):
                    st.write(evento.get("descricao"))

                # Resumo da IA
                if evento.get("resumo"):
                    st.info(f"🤖 Resumo IA: {evento.get('resumo')}")

                # Tags
                if evento.get("tags"):
                    tags = evento.get("tags", "").split(",")
                    st.write("🏷️ Tags:", ", ".join(tags))

            with col2:
                # Tipo de evento
                tipo = evento.get("tipo", "outros")
                tipo_emoji = {
                    "música": "🎵",
                    "cultura": "🎭",
                    "tecnologia": "💻",
                    "esporte": "⚽",
                    "gastronomia": "🍽️",
                    "outros": "🎪",
                }
                st.markdown(f"### {tipo_emoji.get(tipo, '🎪')} {tipo.title()}")

                # Status
                status = evento.get("status", "ativo")
                if status == "ativo":
                    st.success("✅ Ativo")
                elif status == "cancelado":
                    st.error("❌ Cancelado")
                else:
                    st.warning("⏰ Finalizado")

                # Link para mais informações
                if evento.get("url_original"):
                    st.link_button("🔗 Ver Mais", evento.get("url_original"))

            st.divider()

    # Rodapé
    st.markdown("---")
    st.markdown("### 🤖 Funcionalidades de IA")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        **Classificação Automática**
        - Tipos de eventos
        - Categorização inteligente
        """
        )

    with col2:
        st.markdown(
            """
        **Resumos Inteligentes**
        - Descrições otimizadas
        - Pontos principais destacados
        """
        )

    with col3:
        st.markdown(
            """
        **Análise de Sentimento**
        - Público-alvo identificado
        - Tópicos principais extraídos
        """
        )


if __name__ == "__main__":
    main()
