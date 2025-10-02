# 🏗️ Arquitetura kd-Role

## 📋 Visão Geral

kd-Role é uma aplicação simples para buscar eventos com o mínimo de complexidade possível.

## 🎯 Princípios

```mermaid
graph TD
    A[Simplicidade] --> B[Arquivo único]
    A --> C[Endpoints diretos]
    A --> D[Foco em eventos]
    A --> E[Código mínimo]
    
    B --> F[1 Arquivo FastAPI]
    C --> G[APIs RESTful]
    D --> H[Buscar eventos]
    E --> I[~100 linhas total]
```

## 🌐 Arquitetura de Rede

```mermaid
graph LR
    User[👤 User] --> Frontend[🌐 Streamlit Frontend]
    Frontend --> API[⚡ FastAPI :8080]
    API --> DB[(🗃️ SQLite)]
    
    Dev[👨‍💻 Developer] --> CLI[📱 Command Line]
    CLI --> API
    
    subgraph "Container Simples"
        API
        DB
    end
```

## 📦 Fluxo de Dados

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as FastAPI
    participant D as SQLite
    
    U->>F: Seeks events
    F->>A: GET /eventos?cidade=X
    A->>D: SELECT with filter
    D-->>A: Event list
    A-->>F: JSON response
    F-->>U: Display events
```

## 🔧 Stack Tecnologico

```mermaid
pie title Technology Stack
    "FastAPI" : 40
    "SQLite" : 30
    "Streamlit" : 20
    "Python" : 10
```

## 📊 Performance

```mermaid
graph LR
    subgraph "Performance Metrics"
        A[Build Time: 30s] --> B[Startup: 5s]
        B --> C[Response: <100ms]
        C --> D[Memory: 50MB]
    end
```

## 🎭 Endpoints

```mermaid
graph TD
    A[Root /] --> B[GET /eventos]
    A --> C[GET /cidades]
    A --> D[POST /eventos]
    
    B --> E[List Events]
    C --> F[List Cities]
    D --> G[Create Event]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#f3e5f5  
    style D fill:#e8f5e8
```

## 📂 Estrutura Simplificada

```mermaid
graph TD
    A[kd-role/] --> B[eventos.py]
    A --> C[frontend.py]
    A --> D[docker-compose.yml]
    A --> E[Dockerfile]
    A --> F[README.md]
    
    B --> G[FastAPI Core]
    C --> H[Streamlit UI]
    D --> I[Pod Management]
    E --> J[Container Config]
```

---

**🎯 Objetivo**: Arquitetura minimalista que funciona perfeitamente para buscar eventos.
