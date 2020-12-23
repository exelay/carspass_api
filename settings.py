import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = 'carspass'
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
