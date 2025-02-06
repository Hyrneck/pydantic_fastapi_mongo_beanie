# index.py
from mangum import Mangum
from fastapi_pydantic_mongo_beanie_anthony_shea.main import app

# Create the handler for AWS Lambda
handler = Mangum(app)  # Removed lifespan="off" as it might not be needed with older version
