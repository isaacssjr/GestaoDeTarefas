#!/bin/bash

echo "=========================================="
echo "   Gestao de Atividades TI - Instalador"
echo "=========================================="
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python 3 não encontrado! Instale o Python 3.8+."
    exit 1
fi

echo "[1/4] Criando ambiente virtual (.venv)..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
else
    echo "Ambiente virtual já existe."
fi

echo "[2/4] Ativando ambiente e atualizando pip..."
source .venv/bin/activate
python -m pip install --upgrade pip --quiet

echo "[3/4] Instalando dependências..."
pip install -r requirements.txt

echo "[4/4] Testando a aplicação..."
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK!')"

echo ""
echo "=========================================="
echo "   Instalação concluída!"
echo "=========================================="
echo ""
echo "Para executar o sistema:"
echo "  source .venv/bin/activate"
echo "  python main.py"
echo ""
echo "Para compilar para .exe (Linux):"
echo "  pyinstaller --onefile --windowed --name 'GestaoAtividades' main.py"
echo ""
