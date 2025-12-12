#!/bin/bash

echo "========================================"
echo "  Extracao de Blocos - EAP Automacao"
echo "========================================"
echo ""
echo "Verificando Python..."

if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python nao encontrado!"
    echo ""
    echo "Por favor, instale o Python 3.8 ou superior."
    exit 1
fi

echo "Python encontrado!"
echo ""
echo "Instalando dependencias..."
python3 -m pip install --upgrade pip --quiet
python3 -m pip install flask openpyxl --quiet

if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao instalar dependencias!"
    exit 1
fi

echo ""
echo "Dependencias instaladas!"
echo ""
echo "Iniciando servidor..."
echo ""
echo "========================================"
echo "  Servidor rodando em:"
echo "  http://localhost:5000"
echo "========================================"
echo ""
echo "Pressione CTRL+C para parar o servidor"
echo ""
echo ""

python3 web_frontend.py

