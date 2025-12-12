def handler(request):
    """Handler de teste simples"""
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': '{"message": "Handler funcionando!"}'
    }

