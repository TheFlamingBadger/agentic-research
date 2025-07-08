from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import certifi
import os

load_dotenv(find_dotenv())

# Check if environment variables are set
USER_NAME = os.environ.get("MONGODB_USER")
PASSWORD = os.environ.get("MONGODB_PWD")
CLUSTER = os.environ.get("MONGODB_CLUSTER")

connection_string = f"mongodb+srv://{USER_NAME}:{PASSWORD}@{CLUSTER}.ef1ihgu.mongodb.net/?retryWrites=true&w=majority&appName={CLUSTER}"
client = MongoClient(connection_string, tlsCAFile=certifi.where())

def get_db():
    try:
        db = client['sample_mflix']
        return db
    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)
