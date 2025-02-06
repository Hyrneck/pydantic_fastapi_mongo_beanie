# index.py
import sys
import os
from mangum import Mangum
from fastapi import FastAPI

# Debug prints
print("Current working directory:", os.getcwd())
print("Directory contents:", os.listdir())
print("Python path:", sys.path)

try:
    print("Attempting to import app...")
    from fastapi_pydantic_mongo_beanie_anthony_shea.main import app
    print("App imported successfully")
    print("App type:", type(app))
    print("App class:", app.__class__.__name__)
    
    # Create a test route to verify app is working
    @app.get("/debug")
    async def debug():
        return {
            "status": "ok",
            "cwd": os.getcwd(),
            "python_path": sys.path,
            "app_type": str(type(app))
        }

except Exception as e:
    print("Import error:", str(e))
    print("Error type:", type(e))
    
    # Create a fallback app for debugging
    app = FastAPI()
    
    @app.get("/error")
    async def error():
        return {
            "error": str(e),
            "error_type": str(type(e)),
            "cwd": os.getcwd(),
            "python_path": sys.path
        }

# Create the handler for AWS Lambda
handler = Mangum(app, lifespan="off")
