import os
import sys

from vercel_wsgi import handle_request

# Garantir que o diretório raiz esteja no sys.path para importar web_frontend
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from web_frontend import app  # noqa: E402


def handler(request, context):
    return handle_request(app, request, context)

