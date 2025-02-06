# index.py
from mangum import Mangum
from fastapi_pydantic_mongo_beanie_anthony_shea.main import app

handler = Mangum(app, lifespan="off")

