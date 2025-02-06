# vercel/api/index.py
from fastapi import FastAPI
from mangum import Mangum
from fastapi_pydantic_mongo_beanie_anthony_shea.main import app

# Create the handler for AWS Lambda
handler = Mangum(app)

