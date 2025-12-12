"""
Handler para Vercel Serverless Functions - Flask
Formato correto para Vercel Python
A Vercel detecta automaticamente aplicações Flask quando exportadas como 'app'
"""
import os
import sys

# Adicionar diretório raiz ao path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Importar o app Flask
# A Vercel detecta automaticamente aplicações Flask quando exportadas como 'app'
try:
    from web_frontend import app
except Exception as e:
    # Se houver erro na importação, criar um app mínimo para debug
    from flask import Flask
    import traceback
    
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return f'''
        <html>
        <head><title>Erro de Importação</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h1>❌ Erro ao carregar aplicação</h1>
            <p><strong>Erro:</strong> {str(e)}</p>
            <details>
                <summary>Detalhes técnicos</summary>
                <pre style="background: #f5f5f5; padding: 10px; overflow: auto;">{traceback.format_exc()}</pre>
            </details>
        </body>
        </html>
        ''', 500

# Exportar o app diretamente - a Vercel faz o wrapper WSGI automaticamente
# Não precisa de função handler() customizada
