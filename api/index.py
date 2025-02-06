# api/index.py
from fastapi import FastAPI
from mangum import Mangum
import sys
import os

# Add the root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi_pydantic_mongo_beanie_anthony_shea.main import app

# Create the handler for AWS Lambda
handler = Mangum(app)

