#!/bin/bash
# kd-Role - Stop Everything & Cleanup

echo "🛑 kd-Role - STOPPING ALL"
echo "=========================================="

# Verificar se está no diretório correto
if [ ! -f "eventos.py" ]; then
    echo "❌ Execute este script no diretório do projeto"
    exit 1
fi

echo "🔄 Parando processos Python..."

# 1. Parar processos Python local
echo "🐍 Matando processos Python..."
pkill -f eventos.py 2>/dev/null && echo "✅ API Python parou" || echo "⚠️ API Python já parada"
pkill -f streamlit 2>/dev/null && echo "✅ Streamlit parou" || echo "⚠️ Streamlit já parado"

sleep 2

echo ""
echo "🐳 Limpando containers Podman..."

# 2. Parar e remover containers Podman Compose
if command -v podman-compose &> /dev/null; then
    echo "📦 Parando podman-compose..."
    podman-compose down --volumes --remove-orphans 2>/dev/null && echo "✅ Podman-compose parado" || echo "⚠️ Podman-compose já parado"
fi

sleep 2

echo ""
echo "🧹 Limpeza completa do ambiente..."

# 3. Limpar containers órfãos
echo "🗑️ Removendo containers órfãos..."
podman container prune -f 2>/dev/null && echo "✅ Containers órfãos removidos" || echo "⚠️ Nenhum container órfão"

# 4. Limpar volumes órfãos  
echo "🗑️ Removendo volumes órfãos..."
podman volume prune -f 2>/dev/null && echo "✅ Volumes órfãos removidos" || echo "⚠️ Nenhum volume órfão"

# 5. Limpar redes órfãs
echo "🗑️ Removendo redes órfãs..."
podman network prune -f 2>/dev/null && echo "✅ Redes órfãs removidas" || echo "⚠️ Nenhuma rede órfã"

# 6. Limpar imagens não utilizadas
echo "🗑️ Removendo imagens não utilizadas..."
podman image prune -a -f 2>/dev/null && echo "✅ Imagens removidas" || echo "⚠️ Nenhuma imagem para remover"

sleep 2

echo ""
echo "🔍 Verificando portas liberadas..."

# 7. Verificar se portas estão livres
PORTA_8080=$(lsof -i :8080 2>/dev/null | wc -l)
PORTA_8501=$(lsof -i :8501 2>/dev/null | wc -l)

if [ $PORTA_8080 -eq 0 ]; then
    echo "✅ Porta 8080 (API) liberada"
else
    echo "⚠️ Porta 8080 ainda em uso"
fi

if [ $PORTA_8501 -eq 0 ]; then
    echo "✅ Porta 8501 (Frontend) liberada"
else
    echo "⚠️ Porta 8501 ainda em uso"
fi

echo ""
echo "🌿 Limpeza do ambiente completo!"

# 8. Limpar arquivos temporários (opcional)
echo "🥈 Limpando arquivos temporários..."
rm -f eventos.db-journal 2>/dev/null && echo "✅ Database journal removido" || true

echo ""
echo "✅ kd-Role STOPPED & CLEANED!"
echo "=================="
echo "🎯 Para iniciar novamente:"
echo "   ./start_all.sh"
echo ""
echo "🔍 Status das portas:"
echo "📡 API (8080): $(curl -s http://localhost:8080/ >/dev/null 2>&1 && echo 'EM USO' || echo 'LIBERADA')"
echo "🏠 Frontend (8501): $(curl -s http://localhost:8501/ >/dev/null 2>&1 && echo 'EM USO' || echo 'LIBERADA')"
