import os
from dotenv import load_dotenv

from pymongo import MongoClient

load_dotenv()

PROJECT_NAME = 'carspass'
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

CLIENT = MongoClient(
    f"mongodb+srv://imdb:{MONGO_PASSWORD}@carspass.mskrx.mongodb.net/Carspass?retryWrites=true&w=majority"
)
DB = CLIENT['Carspass']
