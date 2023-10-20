from dotenv import dotenv_values
import logging
from dao.mongodao import WasteManagementDao
from constants.error_message import ErrorMessage
from constants.info_message import InfoMessage
from http_handler.response_handler import ResponseHandler
from fastapi import status
from security.details import get_password_hash
import pandas as pd
from db.create_table import CreateTable


class RequestManager:
    def __init__(self, collection_name):
        self.config = dotenv_values(".env")
        self.logger = logging.getLogger(__name__)
        self.dao = WasteManagementDao(collection_name, self.config["DB_NAME"])

    def find(self, condition: dict):
        res = ResponseHandler()
        try:
            result = self.dao.find(condition)
        except Exception as error:
            self.logger.error(ErrorMessage.DB_SELECT)
            self.logger.error(error)
            raise Exception
        if result:
        # print(condition)
            self.logger.info(InfoMessage.DB_FIND)
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


# class SignUp:
# def __init__(self):
#     self.config = dotenv_values(".env")
#     self.logger = logging.getLogger(__name__)
#     self.dao = WasteManagementDao(collection_name="users", database="Waste")
#
# def sign_up(self, user_info):
#     result = ResponseHandler()
#     email = {"email": user_info['email']}
#     username = {"username": user_info['username']}
#     email_res = self.dao.find(email)
#     username_res = self.dao.find(username)
#     if email_res or username_res:
#         result.set_response({"message": ErrorMessage.ALREADY_EXISTS})
#         result.set_status_code(status.HTTP_400_BAD_REQUEST)
#         return result
#
#     user_info["hashed_password"] = get_password_hash(user_info["password"])
#     user_info.pop("password")
#     try:
#         self.dao.insert_one(user_info)
#         self.logger.info(InfoMessage.DB_INSERT)
#     except Exception as error:
#         self.logger.error(ErrorMessage.DB_INSERT)
#         self.logger.error(error)
#         raise Exception
#
#     result.set_response({"message": InfoMessage.DB_INSERT})
#     result.set_status_code(status.HTTP_201_CREATED)
#
#     return result


class FormManager:
    def __init__(self):
        self.config = dotenv_values(".env")
        self.logger = logging.getLogger(__name__)
        self.req = RequestManager(self.config['FORM_STRUCTURE_DB_COLLECTION_NAME'])

    def csv_processor(self):
        tb = CreateTable()
        file_path = 'new_form.csv'
        data = pd.read_csv(file_path)
        dict_data = data.to_dict('records')
        pattern = dict_data[0]
        res = self.req.insert(pattern)
        if res.generate_response().status_code == status.HTTP_400_BAD_REQUEST:
            self.logger.info(InfoMessage.UPDATE_FORM)
            self.req.delete({"form_id": pattern["form_id"]})
            self.req.insert(pattern)
            self.logger.info(InfoMessage.DB_UPDATED)
            res = ResponseHandler()
            res.set_response({"message": InfoMessage.DB_UPDATED})
            res.set_status_code(status.HTTP_200_OK)
        tb.open_csv()
        tb.create_table()

        return res
