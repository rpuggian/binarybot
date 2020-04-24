import logging

class Configuracoes:
    def __init__(self):
        super().__init__()

    def setAtivo(self, ativo):
        if len(ativo) <= 0:
            logging.error("Ativo nao reconhecido")
            return False
        else:
            logging.info("Ativo definido como {}".format(str(ativo)))
            self.ativo=ativo
            return True

    def getAtivo(self):
        return self.ativo

    def setTimeframe(self, timeframe):
        try:
            timeframe=int(timeframe)
        except:
            logging.error("Timeframe nao reconhecido")
            return False
        if isinstance(timeframe, int):
            if int(timeframe) == 5 or int(timeframe) == 1:
                logging.info(
                    "Timeframe definido para {} minutos".format(str(timeframe)))
                self.timeframe=timeframe
                return True
            else:
                logging.error("O timeframe pode ser apenas de 1 ou 5 minutos")
                return False
        else:
            logging.error("Timeframe nao reconhecido")
            return False

    def getTimeframe(self):
        return self.timeframe

    def setPosicao(self, posicao):
        try:
            posicao=int(posicao)
        except:
            logging.error("Posicao nao reconhecido")
            return False
        if isinstance(posicao, int):
            self.posicao=posicao
            logging.info("Posicao definida para {}".format(str(posicao)))
            return True
        else:
            logging.error("Posicao nao reconhecido")
            return False

    def getPosicao(self):
        return self.posicao