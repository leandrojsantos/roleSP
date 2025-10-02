from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
from datetime import datetime
from contextlib import asynccontextmanager

from .config import (
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
    PORT,
    CORS_ORIGINS,
    CORS_CREDENTIALS,
    CORS_METHODS,
    CORS_HEADERS,
    ENVIRONMENT,
)
from .models import create_db_and_tables
from .routers import eventos, scraping, ia

startup_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


class HealthResponse(BaseModel):
    status: str
    uptime: float
    timestamp: str


app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

app.include_router(eventos.router)
app.include_router(scraping.router)
app.include_router(ia.router)


@app.get("/", response_model=dict)
async def root():
    from datetime import datetime

    return {
        "message": f"Welcome to {APP_NAME}!",
        "version": APP_VERSION,
        "docs": "/docs",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/info", response_model=dict)
async def info():
    """Informações detalhadas da aplicação"""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "description": APP_DESCRIPTION,
        "environment": ENVIRONMENT,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="OK",
        uptime=time.time() - startup_time,
        timestamp=datetime.now().isoformat(),
    )


def main():
    """Main function to run the application"""
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
