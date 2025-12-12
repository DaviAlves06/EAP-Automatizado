@echo off
chcp 65001 >nul
echo ========================================
echo   Extracao de Blocos - EAP Automacao
echo ========================================
echo.
echo Verificando Python...

python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo.
    echo Por favor, instale o Python de: https://www.python.org/downloads/
    echo Certifique-se de marcar "Add Python to PATH" durante a instalacao.
    pause
    exit /b 1
)

echo Python encontrado!
echo.
echo Instalando dependencias...
python -m pip install --upgrade pip --quiet
python -m pip install flask openpyxl --quiet

if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo Dependencias instaladas!
echo.
echo Iniciando servidor...
echo.
echo ========================================
echo   Servidor rodando em:
echo   http://localhost:5000
echo ========================================
echo.
echo Pressione CTRL+C para parar o servidor
echo.
echo.

python web_frontend.py

pause

