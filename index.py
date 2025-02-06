# index.py
from fastapi_pydantic_mongo_beanie_anthony_shea.main import app

async def handler(event, context):
    if event.get('version') == '2.0':
        return await handle_aws_v2(event, context)
    return await handle_aws_v1(event, context)

async def handle_aws_v1(event, context):
    import asyncio
    from urllib.parse import urlencode

    path = event['path']
    http_method = event['httpMethod']
    headers = event['headers'] or {}
    query_string = urlencode(event['queryStringParameters'] or {})
    body = event.get('body', '')
    is_base64_encoded = event.get('isBase64Encoded', False)

    if is_base64_encoded:
        import base64
        body = base64.b64decode(body)

    scope = {
        'type': 'http',
        'method': http_method,
        'headers': [[k.lower().encode(), v.encode()] for k, v in headers.items()],
        'path': path,
        'raw_path': path.encode(),
        'query_string': query_string.encode(),
        'server': ('vercel', None),
        'client': ('', 0),
        'scheme': 'https',
        'asgi': {'version': '3.0'},
        'root_path': '',
    }

    response = {}
    body_parts = []

    async def receive():
        return {
            'type': 'http.request',
            'body': body.encode() if isinstance(body, str) else body,
            'more_body': False,
        }

    async def send(message):
        if message['type'] == 'http.response.start':
            response['statusCode'] = message['status']
            response['headers'] = {k.decode(): v.decode() for k, v in message['headers']}
        elif message['type'] == 'http.response.body':
            body_parts.append(message.get('body', b''))

    await app(scope, receive, send)
    
    response_body = b''.join(body_parts)
    if any(response['headers'].get(h, '').lower() == 'base64' 
           for h in ('content-transfer-encoding', 'content-encoding')):
        import base64
        response['body'] = base64.b64encode(response_body).decode()
        response['isBase64Encoded'] = True
    else:
        response['body'] = response_body.decode()
        response['isBase64Encoded'] = False

    return response

async def handle_aws_v2(event, context):
    import base64
    from urllib.parse import urlencode

    request_context = event['requestContext']
    headers = event.get('headers', {})
    raw_query_string = event.get('rawQueryString', '')
    body = event.get('body', '')
    is_base64_encoded = event.get('isBase64Encoded', False)

    if is_base64_encoded and body:
        body = base64.b64decode(body)

    scope = {
        'type': 'http',
        'method': request_context['http']['method'],
        'headers': [[k.lower().encode(), v.encode()] for k, v in headers.items()],
        'path': event['rawPath'],
        'raw_path': event['rawPath'].encode(),
        'query_string': raw_query_string.encode(),
        'server': ('vercel', None),
        'client': ('', 0),
        'scheme': 'https',
        'asgi': {'version': '3.0'},
        'root_path': '',
    }

    response = {}
    body_parts = []

    async def receive():
        return {
            'type': 'http.request',
            'body': body.encode() if isinstance(body, str) else body,
            'more_body': False,
        }

    async def send(message):
        if message['type'] == 'http.response.start':
            response['statusCode'] = message['status']
            response['headers'] = {k.decode(): v.decode() for k, v in message['headers']}
        elif message['type'] == 'http.response.body':
            body_parts.append(message.get('body', b''))

    await app(scope, receive, send)
    
    response_body = b''.join(body_parts)
    if any(response['headers'].get(h, '').lower() == 'base64' 
           for h in ('content-transfer-encoding', 'content-encoding')):
        response['body'] = base64.b64encode(response_body).decode()
        response['isBase64Encoded'] = True
    else:
        response['body'] = response_body.decode()
        response['isBase64Encoded'] = False

    return response

