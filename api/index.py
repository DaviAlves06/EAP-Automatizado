"""
Handler para Vercel Serverless Functions
Formato simplificado e robusto
"""
import os
import sys
import traceback

# Adicionar diretório raiz ao path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Tentar importar o app Flask
try:
    from web_frontend import app
    APP_LOADED = True
    print("✅ App Flask carregado com sucesso")
except Exception as e:
    APP_LOADED = False
    ERROR_MESSAGE = str(e)
    ERROR_TRACE = traceback.format_exc()
    print(f"❌ ERRO ao importar web_frontend: {ERROR_MESSAGE}")
    print(ERROR_TRACE)


def handler(request):
    """
    Handler principal para Vercel
    Converte requisições da Vercel para WSGI e executa o app Flask
    """
    # Se o app não foi carregado, retornar erro informativo
    if not APP_LOADED:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/html; charset=utf-8'},
            'body': f'''
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
            '''
        }
    
    from io import BytesIO
    from urllib.parse import urlparse
    
    try:
        # Extrair informações básicas da requisição
        method = getattr(request, 'method', 'GET') or 'GET'
        
        # Obter path
        path = '/'
        if hasattr(request, 'path') and request.path:
            path = request.path
        elif hasattr(request, 'url'):
            url_val = request.url
            if isinstance(url_val, str):
                parsed = urlparse(url_val)
                path = parsed.path or '/'
        
        if not path or not path.startswith('/'):
            path = '/'
        
        # Query string
        query_string = ''
        if hasattr(request, 'query'):
            q = request.query
            if isinstance(q, dict):
                from urllib.parse import urlencode
                query_string = urlencode(q)
            elif isinstance(q, str):
                query_string = q
        
        # Body
        body = b''
        if hasattr(request, 'body'):
            body_val = request.body
            if body_val:
                if isinstance(body_val, str):
                    body = body_val.encode('utf-8')
                elif isinstance(body_val, bytes):
                    body = body_val
                else:
                    body = str(body_val).encode('utf-8')
        
        # Headers
        content_type = ''
        headers_dict = {}
        if hasattr(request, 'headers'):
            h = request.headers
            if isinstance(h, dict):
                headers_dict = h
                content_type = h.get('content-type', '')
            elif hasattr(h, 'get'):
                content_type = h.get('content-type', '')
                headers_dict = {k: h.get(k) for k in ['content-type', 'content-length'] if h.get(k)}
        
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
        
        # Adicionar headers HTTP ao environ
        for key, value in headers_dict.items():
            if key.lower() not in ('content-type', 'content-length'):
                key_upper = key.upper().replace('-', '_')
                environ[f'HTTP_{key_upper}'] = str(value)
        
        # Preparar resposta
        status_code = [200]
        headers_list = []
        body_parts = []
        
        def start_response(status_line, response_headers):
            status_code[0] = int(status_line.split()[0])
            headers_list.extend(response_headers)
        
        # Executar app Flask
        result = app(environ, start_response)
        
        # Coletar resposta
        for part in result:
            if isinstance(part, bytes):
                body_parts.append(part)
            else:
                body_parts.append(part.encode('utf-8'))
        
        response_body = b''.join(body_parts)
        
        # Converter headers para dicionário
        response_headers = {}
        for header, value in headers_list:
            response_headers[header] = value
        
        # Retornar no formato que a Vercel espera
        return {
            'statusCode': status_code[0],
            'headers': response_headers,
            'body': response_body.decode('utf-8', errors='ignore')
        }
        
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"❌ ERRO no handler: {str(e)}")
        print(error_trace)
        
        # Retornar erro no formato correto
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': f'{{"success": false, "error": "Erro interno do servidor: {str(e)}"}}'
        }
