# api/index.py
from fastapi_pydantic_mongo_beanie_anthony_shea.main import app
from http.server import BaseHTTPRequestHandler
import json

def handler(request, response):
    """Vercel serverless function handler"""
    # Get the path from the request
    path = request.get('path', '/')
    
    # Use your FastAPI app to generate response
    @app.get(path)
    async def dynamic_route():
        return {"message": "Hello from FastAPI!"}
    
    # Return JSON response
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello from FastAPI!"}),
        "headers": {
            "Content-Type": "application/json"
        }
    }
