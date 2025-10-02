# Frontend EventRadar

Frontend web para a plataforma EventRadar construído com Streamlit.

## Funcionalidades

- 📅 Visualização de eventos com filtros
- 🔍 Busca por cidade, tipo e preço
- 📊 Gráficos e métricas
- 🤖 Integração com IA para resumos
- 📱 Interface responsiva

## Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
streamlit run app.py
```

## Configuração

A aplicação se conecta automaticamente com a API backend na URL `http://localhost:8000`.

Para alterar a URL da API, modifique a variável `API_BASE_URL` no arquivo `app.py`.

## Uso

1. Acesse a aplicação no navegador
2. Use os filtros na sidebar para buscar eventos
3. Visualize métricas e gráficos
4. Explore os eventos encontrados

## Estrutura

- `app.py` - Aplicação principal Streamlit
- `requirements.txt` - Dependências Python
- `README.md` - Documentação

