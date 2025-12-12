import os
import sys

# Adicionar diretório raiz ao path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from web_frontend import app

# A Vercel detecta automaticamente aplicações Flask
# Exportar o app diretamente funciona na maioria dos casos
# Se não funcionar, precisaremos de um wrapper WSGI
