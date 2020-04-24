import os
import datetime
import logging

class Logs:
    def __init__(self):
        super().__init__()
        self.criarPasta()
        self.ativarLog()

    def criarPasta(self):
        if not os.path.exists("Logs/"):
            os.mkdir("Logs")

    def ativarLog(self):
        arquivo = "Logs/{}.log".format(
            datetime.datetime.now().strftime("%d-%m-%Y"))
        level = logging.INFO
        formato = "%(asctime)s %(levelname)s: %(message)s"
        data = "%d-%m-%Y %H:%M:%S"
        logging.basicConfig(filename=arquivo, level=level,
                            format=formato, datefmt=data)