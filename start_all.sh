#!/bin/bash
# kd-Role - Start Everything

echo "🚀 kd-Role Startup"
echo "=================================="

# Verificar se está no diretório correto
if [ ! -f "eventos.py" ]; then
    echo "❌ Execute este script no diretório do projeto"
    exit 1
fi

# 1. Iniciar API (Podman ou Local)
echo "📡 Iniciando API..."
if command -v podman-compose &> /dev/null; then
    echo "🐳 Usando Podman Compose..."
    podman-compose up --build -d
    sleep 5
else
    echo "🐍 Usando Python local..."
        pip install fastapi uvicorn requests streamlit 2>/dev/null || echo "Dependências já instaladas"
        python eventos.py &
    sleep 3
fi

# 2. Iniciar Frontend
echo "🌐 Iniciando Frontend..."
streamlit run frontend.py --server.port 8501 --server.headless true &

sleep 5

echo ""
echo "✅ kd-Role funcionando!"
echo "⚡ URLs disponíveis:"
echo "🌐 API: http://localhost:8080"
echo "📚 Docs: http://localhost:8080/docs"
echo "🏠 Frontend: http://localhost:8501"
echo ""
echo "🔍 Teste rápido:"
curl -s http://localhost:8080/ | python -c "import sys, json; print(json.load(sys.stdin)['message'])"
echo ""
echo "💡 Para parar tudo:"
echo "   pkill -f eventos.py"
echo "   pkill -f streamlit"
echo "   podman-compose down"
