"""
Handler para Vercel Serverless Functions - Flask
Seguindo a documentação oficial da Vercel para Python/Flask
"""
import os
import sys
import traceback

# Adicionar diretório raiz ao path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Importar o app Flask
try:
    from web_frontend import app
    APP_LOADED = True
except Exception as e:
    APP_LOADED = False
    ERROR_MESSAGE = str(e)
    ERROR_TRACE = traceback.format_exc()
    print(f"ERRO ao importar web_frontend: {ERROR_MESSAGE}")
    print(ERROR_TRACE)


def handler(req, res):
    """
    Handler WSGI para Vercel Serverless Functions
    Converte requisições da Vercel para formato WSGI do Flask
    """
    # Se o app não foi carregado, retornar erro
    if not APP_LOADED:
        res.status(500)
        res.set_header('Content-Type', 'text/html; charset=utf-8')
        res.send(f'''
        <html>
        <head><title>Erro de Importação</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h1>❌ Erro ao carregar aplicação</h1>
            <p><strong>Erro:</strong> {ERROR_MESSAGE}</p>
            <details>
                <summary>Detalhes técnicos</summary>
                <pre style="background: #f5f5f5; padding: 10px; overflow: auto;">{ERROR_TRACE}</pre>
            </details>
        </body>
        </html>
        ''')
        return
    
    from io import BytesIO
    from urllib.parse import urlparse
    
    try:
        # Extrair informações da requisição da Vercel
        method = getattr(req, 'method', 'GET') or 'GET'
        
        # Path
        path = getattr(req, 'path', '/') or '/'
        if not path.startswith('/'):
            path = '/' + path
        
        # Tratar arquivos estáticos comuns (favicon, robots.txt, etc.)
        # Retornar 404 para evitar processamento desnecessário
        static_files = ['/favicon.ico', '/favicon.png', '/robots.txt', '/apple-touch-icon.png']
        if path.lower() in static_files:
            res.status(404)
            res.set_header('Content-Type', 'text/plain')
            res.send('Not Found')
            return
        
        # Query string
        query_string = ''
        if hasattr(req, 'query'):
            q = req.query
            if isinstance(q, dict):
                from urllib.parse import urlencode
                query_string = urlencode(q)
            elif isinstance(q, str):
                query_string = q
        
        # Body
        body = b''
        if hasattr(req, 'body'):
            body_val = req.body
            if body_val:
                if isinstance(body_val, str):
                    body = body_val.encode('utf-8')
                elif isinstance(body_val, bytes):
                    body = body_val
        
        # Headers
        content_type = ''
        headers_dict = {}
        if hasattr(req, 'headers'):
            h = req.headers
            if isinstance(h, dict):
                headers_dict = h
                content_type = h.get('content-type', '')
            elif hasattr(h, 'get'):
                content_type = h.get('content-type', '')
        
        # Criar ambiente WSGI
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'QUERY_STRING': query_string,
            'CONTENT_TYPE': content_type,
            'CONTENT_LENGTH': str(len(body)),
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': BytesIO(body),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
        }
        
        # Adicionar headers HTTP
        for key, value in headers_dict.items():
            if key.lower() not in ('content-type', 'content-length'):
                key_upper = key.upper().replace('-', '_')
                environ[f'HTTP_{key_upper}'] = str(value)
        
        # Response
        status_code = [200]
        headers_list = []
        body_parts = []
        
        def start_response(status_line, response_headers):
            status_code[0] = int(status_line.split()[0])
            headers_list.extend(response_headers)
        
        # Executar app Flask
        try:
            result = app(environ, start_response)
            
            # Coletar resposta
            for part in result:
                if isinstance(part, bytes):
                    body_parts.append(part)
                else:
                    body_parts.append(part.encode('utf-8'))
            
            response_body = b''.join(body_parts)
            
            # Configurar resposta da Vercel
            res.status(status_code[0])
            for header, value in headers_list:
                res.set_header(header, value)
            res.send(response_body)
            
        except Exception as flask_error:
            # Se o Flask gerar erro, retornar erro 500
            error_trace = traceback.format_exc()
            print(f"ERRO no Flask: {str(flask_error)}")
            print(error_trace)
            
            res.status(500)
            res.set_header('Content-Type', 'application/json')
            res.send(f'{{"success": false, "error": "Erro no processamento: {str(flask_error)}"}}')
        
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"ERRO no handler: {str(e)}")
        print(error_trace)
        
        res.status(500)
        res.set_header('Content-Type', 'application/json')
        res.send(f'{{"success": false, "error": "Erro interno do servidor: {str(e)}"}}')
