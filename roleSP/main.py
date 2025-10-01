from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from datetime import datetime
from typing import Dict, Any

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="{{PROJECT_NAME}}",
    description="{{PROJECT_DESCRIPTION}}",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class HealthResponse(BaseModel):
    status: str
    uptime: float
    timestamp: str


class WelcomeResponse(BaseModel):
    message: str
    version: str
    timestamp: str


@app.get("/", response_model=WelcomeResponse)
async def root():
    """Welcome endpoint"""
    return WelcomeResponse(
        message="Welcome to {{PROJECT_NAME}}!",
        version="1.0.0",
        timestamp=datetime.now().isoformat(),
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    import time

    return HealthResponse(
        status="OK", uptime=time.time(), timestamp=datetime.now().isoformat()
    )


@app.get("/info")
async def get_info():
    """Get application information"""
    return {
        "name": "{{PROJECT_NAME}}",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "python_version": os.sys.version,
        "timestamp": datetime.now().isoformat(),
    }


def main():
    """Main function to run the application"""
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
