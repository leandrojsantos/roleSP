### RoleSP

Uma plataforma completa que busca, filtra, resume e exibe eventos de diversas fontes online com integração de IA para classificação automática e resumos inteligentes.

## ✨ Funcionalidades

- 🔍 **Busca Inteligente**: Filtros por cidade, tipo, preço e data
- 🤖 **IA Integrada**: Classificação automática e resumos com Ollama
- 🕷️ **Scraping Automático**: Coleta de eventos de múltiplas fontes
- 🔐 **Autenticação**: Sistema de usuários simplificado
- 📊 **Frontend Moderno**: Interface web com Streamlit
- 🐳 **Containerização**: Deploy com Podman Compose
- 🧪 **Testes Completos**: 100% de aprovação (41/41 testes)
 aplicados

---

🔧 Backend (100% Python) — API + Scraping + IA

📌 Tecnologias:

| Camada         | Tecnologia                       | Função                                           |
| -------------- | -------------------------------- | ------------------------------------------------ |
| Framework API  | FastAPI                          | Leve, rápido, async, com documentação automática |
| Scraping       | Playwright + Selectolax          | Suporte headless, rápido, anti-bloqueio          |
| IA             | Ollama (Mistral/DeepSeek)        | Resumos e classificação local sem custo          |
| Banco de Dados | PostgreSQL via SQLModel          | Tipado, moderno, ORM + SQL                       |
| Auth           | OAuth2 com FastAPI Users         | Login seguro (caso precise acesso personalizado) |
| Testes         | Pytest + HTTPX                   | Testes automatizados async                       |
| Deploy         | Podman, Podman Compose, Gunicorn | Produção com CI/CD                               |

📄 Endpoints principais:

- GET /eventos: lista eventos
- GET /eventos?cidade=Mauá
- GET /eventos?cidade=São Paulo
- POST /eventos: (interna) adiciona evento do scraper
- GET /eventos/{id}

---


---

🤖 Funcionalidades com IA (via Ollama ou API externa)

- Classificação automática por:
  - Tipo de evento (música, cultura, tecnologia)
  - Cidade, região, se pago ou gratuito
- Resumo da descrição
- Filtros por:
  - Data início/fim
  - Preço
  - Palavras-chave
  - Local

---

📦 Podman Compose (estrutura)

- backend: API + scraper + AI integration
- db: PostgreSQL
- ollama: com modelo local como Mistral ou DeepSeek


---

🧪 Testes
- Cobertura com Pytest
- Testes de API, scraping e normalização dos dados
- Teste automático da IA local se modelo estiver disponível

---



### 🚀 Quick Start (1 comando)

```bash
# Clone e execute
git clone [repo] && cd roleSP && ./run up
```

### 🎯 Script Único

```bash
./run up      # Subir tudo
./run down    # Parar  
./run logs    # Ver logs
./run status  # Status
./run clean   # Limpar
```

### 🌐 Acesso Direto

- **App**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## 🛠️ Tecnologias

- **Backend**: FastAPI, SQLModel, PostgreSQL
- **IA**: Ollama (Mistral/DeepSeek)
- **Scraping**: Playwright, Selectolax
- **Frontend**: Streamlit
- **Containerização**: Podman
- **Testes**: Pytest, HTTPX
