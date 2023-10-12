import pymongo
import logging
from constants.error_message import ErrorMessage
from dotenv import dotenv_values


class DBconnect:
    def __init__(self, collection, database):
        self.database = database
        self.collection = collection
        self.config = dotenv_values(".env")
        self.logger = logging.getLogger(__name__)

    def connect(self):

        try:
            client = pymongo.MongoClient(self.config['DB_HOST'], int(self.config['DB_PORT']))
        except Exception as error:
            self.logger.error(ErrorMessage.DB_CONNECTION)
            self.logger.error(error)
            raise Exception

        try:
            database = client[self.database]
            collection = database[self.collection]
        except Exception as error:
            self.logger.error(ErrorMessage.DB_CONNECTION)
            self.logger.error(error)
            raise Exception

        return collection
