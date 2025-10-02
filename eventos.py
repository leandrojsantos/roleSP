"""
kd-Role - Apenas buscar eventos
Simples e direto
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

app = FastAPI(title="kd-Role")

# Database simples
DB_FILE = "eventos.db"


def init_db():
    """Inicializar banco simples"""
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            cidade TEXT NOT NULL,
            data TEXT NOT NULL,
            url TEXT
        )
    """
    )
    conn.commit()
    conn.close()


class Evento(BaseModel):
    id: Optional[int] = None
    nome: str
    cidade: str
    data: str
    url: Optional[str] = None


@app.get("/")
def root():
    return {"message": "kd-Role - Buscar Eventos"}


@app.get("/eventos", response_model=List[Evento])
def listar_eventos(cidade: Optional[str] = None, limite: int = 50):
    """Listar eventos - pode filtrar por cidade"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    if cidade:
        query = "SELECT * FROM eventos WHERE cidade LIKE ? LIMIT ?"
        params = (f"%{cidade}%", limite)
        cursor.execute(query, params)
    else:
        cursor.execute("SELECT * FROM eventos LIMIT ?", (limite,))

    eventos = []
    for row in cursor.fetchall():
        evento_data = {
            "id": row[0],
            "nome": row[1],
            "cidade": row[2],
            "data": row[3],
            "url": row[4],
        }
        eventos.append(Evento(**evento_data))

    conn.close()
    return eventos


@app.post("/eventos", response_model=dict)
def criar_evento(evento: Evento):
    """Adicionar evento"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO eventos (nome, cidade, data, url) VALUES (?, ?, ?, ?)",
        (evento.nome, evento.cidade, evento.data, evento.url),
    )

    conn.commit()
    conn.close()

    return {"mensagem": "Evento criado com sucesso"}


@app.get("/cidades", response_model=List[str])
def listar_cidades():
    """Listar cidades únicas"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT cidade FROM eventos ORDER BY cidade")
    cidades = [row[0] for row in cursor.fetchall()]
    conn.close()
    return cidades


# Inicializar na startup
@app.on_event("startup")
async def startup_event():
    init_db()

    # Adicionar alguns eventos de exemplo
    eventos_exemplo = [
        ("Show Rock SP", "São Paulo", "2025-01-20", "https://exemplo.com"),
        ("Palestra Tech", "São Paulo", "2025-01-25", ""),
        ("Festival Rio", "Rio de Janeiro", "2025-02-15", ""),
    ]

    conn = sqlite3.connect(DB_FILE)
    for evento in eventos_exemplo:
        conn.execute(
            "INSERT OR IGNORE INTO eventos "
            "(nome, cidade, data, url) VALUES (?, ?, ?, ?)",
            evento,
        )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("eventos:app", host="0.0.0.0", port=8080, reload=False)
