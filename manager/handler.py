from dotenv import dotenv_values
import logging
from dao.mongodao import WasteManagementDao
from constants.error_message import ErrorMessage
from constants.info_message import InfoMessage
from http_handler.response_handler import ResponseHandler
from fastapi import status


class RequestManager:
    def __init__(self):
        self.config = dotenv_values(".env")
        self.logger = logging.getLogger(__name__)
        self.dao = WasteManagementDao(self.config['DB_COLLECTION_NAME'], self.config["DB_NAME"])

    def find(self, condition: dict):
        res = ResponseHandler()
        try:
            result = self.dao.find(condition)
            self.logger.info(InfoMessage.DB_FIND)
        except Exception as error:
            self.logger.error(ErrorMessage.DB_SELECT)
            self.logger.error(error)
            raise Exception
        if result:
            res.set_response(result)
            res.set_status_code(status.HTTP_200_OK)
            return res

        res.set_response({"message": InfoMessage.NOT_FOUND})
        res.set_status_code(status.HTTP_404_NOT_FOUND)

        return res

    def insert(self, doc: dict):
        res = ResponseHandler()
        form_id = {"form_id": doc['form_id']}
        duplicate_check = self.find(form_id)
        if duplicate_check.generate_response().status_code == status.HTTP_200_OK:
            res.set_response({"message": ErrorMessage.ALREADY_EXISTS})
            res.set_status_code(status.HTTP_400_BAD_REQUEST)
            return res

        try:
            self.dao.insert_one(doc)
            self.logger.info(InfoMessage.DB_INSERT)
        except Exception as error:
            self.logger.error(ErrorMessage.DB_INSERT)
            self.logger.error(error)
            raise Exception

        res.set_response({"message": InfoMessage.DB_INSERT})
        res.set_status_code(status.HTTP_201_CREATED)

        return res

    def update(self, form_id, doc: dict):
        res = ResponseHandler()
        duplicate_check = self.find(form_id)
        if duplicate_check.generate_response().status_code == status.HTTP_404_NOT_FOUND:
            res.set_response({"message": ErrorMessage.NOT_FOUND})
            res.set_status_code(status.HTTP_400_BAD_REQUEST)
            return res

        try:
            self.dao.update(fltr=form_id, new_values=doc)
            self.logger.info(InfoMessage.DB_UPDATED)
        except Exception as error:
            self.logger.error(ErrorMessage.DB_UPDATE)
            self.logger.error(error)
            raise Exception

        res.set_response({"message": InfoMessage.DB_UPDATED})
        res.set_status_code(status.HTTP_200_OK)

        return res

    def delete(self, doc):
        res = ResponseHandler()

        duplicate_check = self.find(doc)
        if duplicate_check.generate_response().status_code == status.HTTP_404_NOT_FOUND:
            res.set_response({"message": ErrorMessage.NOT_FOUND})
            res.set_status_code(status.HTTP_400_BAD_REQUEST)
            return res

        try:
            self.dao.delete(doc)
            self.logger.info(InfoMessage.DB_DELETE)
        except Exception as error:
            self.logger.error(ErrorMessage.DB_DELETE)
            self.logger.error(error)
            raise Exception

        res.set_response({"message": InfoMessage.DB_DELETE})
        res.set_status_code(status.HTTP_200_OK)

        return res

    def check_action(self, req):
        if req['action'] == "add":
            res = self.insert(req["payload"])
        if req['action'] == "update":
            res = self.update(req["form_id"], req["payload"])
        if req['action'] == "delete":
            res = self.delete(req["form_id"])
        if req['action'] == "get":
            res = self.find({"form_id": req["form_id"]})
        else:
            res = None
        return res
