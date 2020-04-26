import os
import datetime
import logging


class Logs:
    def __init__(self):
        super().__init__()
        self.create_folder()
        self.build_files()

    @staticmethod
    def print_message(message):
        logging.info(message)
        print(message)

    @staticmethod
    def print_error(message):
        logging.error(message)
        print(message)

    @staticmethod
    def create_folder():
        if not os.path.exists("Logs/"):
            os.mkdir("Logs")

    @staticmethod
    def build_files():
        file = "Logs/{}.log".format(
            datetime.datetime.now().strftime("%d-%m-%Y"))
        format = "%(asctime)s %(levelname)s: %(message)s"
        date = "%d-%m-%Y %H:%M:%S"
        logging.basicConfig(filename=file, level=logging.INFO,
                            format=format, datefmt=date)
