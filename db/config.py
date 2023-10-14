import pymongo
from dotenv import dotenv_values
import logging

config = dotenv_values(".env")
logger = logging.getLogger(__name__)

print(config['DB_HOST'])
client = pymongo.MongoClient(host=str(config['DB_HOST']),port= int(config['DB_PORT']))
logger.info("Connecting to database...")
db = client["test"]
User = db.users
Form = db.forms
User.create_index([("email", pymongo.ASCENDING)], unique=True)
Form.create_index([("title", pymongo.ASCENDING)], unique=True)
