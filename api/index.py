import os
import sys
from io import BytesIO

# Adicionar diretório raiz ao path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from web_frontend import app


def handler(req, res):
    """
    Handler WSGI para Vercel Serverless Functions
    Converte requisições da Vercel para formato WSGI do Flask
    """
    from urllib.parse import parse_qs, urlparse
    
    try:
        # Parse da URL - lidar com diferentes formatos
        path = getattr(req, 'path', '/')
        if not path or path == '':
            path = req.url.split('?')[0] if hasattr(req, 'url') else '/'
        
        # Garantir que path começa com /
        if not path.startswith('/'):
            path = '/' + path
        
        parsed = urlparse(path)
        path = parsed.path
        query_string = parsed.query or ''
        
        # Ler body se existir
        body = b''
        if hasattr(req, 'body'):
            body = req.body or b''
        elif hasattr(req, 'payload'):
            body = req.payload or b''
        
        if isinstance(body, str):
            body = body.encode('utf-8')
    except Exception as e:
        res.status(500)
        res.set_header('Content-Type', 'application/json')
        res.send(f'{{"success": false, "error": "Erro ao processar requisição: {str(e)}"}}'.encode('utf-8'))
        return
    
    # Obter método HTTP
    method = getattr(req, 'method', 'GET')
    if not method:
        method = 'GET'
    
    # Obter content-type
    content_type = ''
    if hasattr(req, 'headers'):
        if isinstance(req.headers, dict):
            content_type = req.headers.get('content-type', '')
        elif hasattr(req.headers, 'get'):
            content_type = req.headers.get('content-type', '')
    
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
    headers_dict = {}
    if hasattr(req, 'headers'):
        if isinstance(req.headers, dict):
            headers_dict = req.headers
        elif hasattr(req.headers, 'items'):
            headers_dict = dict(req.headers.items())
        elif hasattr(req.headers, 'get'):
            # Se for um objeto com método get, tentar extrair headers comuns
            for common_header in ['content-type', 'content-length', 'user-agent', 'accept']:
                val = req.headers.get(common_header)
                if val:
                    headers_dict[common_header] = val
    
    for key, value in headers_dict.items():
        key_upper = key.upper().replace('-', '_')
        if key_upper not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key_upper}'] = str(value)
    
    # Response
    status_code = [200]
    headers = []
    body_parts = []
    
    def start_response(status_line, response_headers):
        status_code[0] = int(status_line.split()[0])
        headers.extend(response_headers)
    
    # Executar app Flask
    try:
        result = app(environ, start_response)
        body_parts = [part for part in result]
    except Exception as e:
        # Em caso de erro, retornar erro 500
        status_code[0] = 500
        headers = [('Content-Type', 'application/json')]
        body_parts = [f'{{"success": false, "error": "Erro interno: {str(e)}"}}'.encode('utf-8')]
    
    # Montar resposta
    response_body = b''.join(body_parts)
    
    # Configurar resposta da Vercel
    res.status(status_code[0])
    for header, value in headers:
        res.set_header(header, value)
    res.send(response_body)
