import csv
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from dotenv import dotenv_values
import logging


# Dictionary containing column names as keys
class CreateTable:
    def __init__(self):

        self.config = dotenv_values(".env")
        self.logger = logging.getLogger(__name__)
        self.data_rows = None
        self.column_names = None

    def open_csv(self):
        with open("new_form.csv", 'r') as file:
            csv_reader = csv.reader(file)
            self.column_names = next(csv_reader)  # Assumes the first row contains column names
            self.data_rows = list(csv_reader)  # Assumes the remaining rows contain data values

    def create_table(self):
        engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{db}'.format(
            user=self.config["DB_USER"], password=self.config["DB_PASSWORD"], host=self.config["PG_DB_HOST"],
            port=self.config["PG_DB_PORT"],db=self.config["DB_DATABASE"]
        ))

        # Declare a base class for our models
        Base = declarative_base()

        # Generate the model class dynamically
        TableClass = type(
            'MyTable',
            (Base,),
            {"__tablename__": 'my_table',
             'id': Column(Integer, primary_key=True),
             **{self.column_names: Column(String)
                for self.column_names in self.column_names}}
        )

        # Create the table in the database
        Base.metadata.create_all(engine)
