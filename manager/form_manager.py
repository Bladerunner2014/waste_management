from dotenv import dotenv_values
import logging
from dao.mongodao import WasteManagementDao
from constants.error_message import ErrorMessage
from constants.info_message import InfoMessage
from http_handler.response_handler import ResponseHandler
from fastapi import status


class FormManager:
    def __init__(self):
        self.config = dotenv_values(".env")
        self.logger = logging.getLogger(__name__)
        self.dao = WasteManagementDao(self.config['DB_COLLECTION_NAME'], self.config["DB_NAME"])
