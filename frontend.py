"""
Frontend MINIMAL para kd-Role
Apenas buscar eventos de forma simples
"""

import streamlit as st
import requests
from typing import List, Dict, Optional

st.set_page_config(page_title="kd-Role", layout="wide")

API_URL = "http://localhost:8080"


def buscar_eventos(cidade: Optional[str] = None) -> List[Dict]:
    """Buscar eventos na API"""
    try:
        if cidade:
            url = f"{API_URL}/eventos?cidade={cidade}"
            response = requests.get(url)
        else:
            response = requests.get(f"{API_URL}/eventos")

        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []


def buscar_cidades() -> List[str]:
    """Buscar cidades disponíveis"""
    try:
        response = requests.get(f"{API_URL}/cidades")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []


st.title("🎭 kd-Role")
st.subheader("Buscar eventos - SIMPLES")

# Filtros
col1, col2 = st.columns(2)

with col1:
    cidades = buscar_cidades()
    cidade_select = st.selectbox("🏙️ Cidade", ["Todas"] + cidades)

with col2:
    if st.button("🔍 Buscar"):
        st.rerun()

# Buscar eventos
cidade_filtro = cidade_select if cidade_select != "Todas" else None
eventos = buscar_eventos(cidade_filtro)

# Mostrar resultado
st.markdown("---")

if eventos:
    st.success(f"📅 Encontrados {len(eventos)} eventos")

    for evento in eventos:
        with st.container():
            st.markdown(
                f"""
            ### 📍 {evento['nome']}
            **Cidade:** {evento['cidade']}  
            **Data:** {evento['data']}  
            {f"**URL:** {evento['url']}" if evento['url'] else ""}
            """
            )
            st.markdown("---")
else:
    st.warning("⚠️ Nenhum evento encontrado")

    # Tentar adicionar evento de exemplo
    if st.button("➕ Adicionar Evento de Exemplo"):
        exemplo = {
            "nome": "Evento Demo",
            "cidade": "São Paulo",
            "data": "2025-12-31",
            "url": "https://exemplo.com",
        }

        try:
            response = requests.post(f"{API_URL}/eventos", json=exemplo)
            if response.status_code == 200:
                st.success("✅ Evento adicionado!")
                st.rerun()
        except Exception:
            st.error("❌ Erro ao adicionar evento")

# Status da API
st.markdown("---")
st.markdown("🔧 **Status:**")
try:
    response = requests.get(f"{API_URL}/")
    st.success("✅ API Online")
except Exception:
    st.error("❌ API Offline")
