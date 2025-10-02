FROM python:3.11-slim

WORKDIR /app

# Instalar apenas o necessário
RUN pip install fastapi uvicorn requests

# Copiar apenas o arquivo principal
COPY eventos.py .

# Criar usuário seguro
RUN useradd app && chown -R app:app /app
USER app

EXPOSE 8080

# Comando simples
CMD ["python", "eventos.py"]
