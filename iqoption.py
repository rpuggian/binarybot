from iqoptionapi.stable_api import IQ_Option
import schedule
import logging
from logs import Logs

logs = Logs()


class IQOption:
    def __init__(self, email, senha):
        super().__init__()
        self.email = email
        self.senha = senha
        self.api = IQ_Option(self.email, self.senha)

    def definirConfiguracoes(self, ativo, timeframe, posicao):
        self.ativo = ativo
        self.timeframe = int(timeframe)
        self.posicao = int(posicao)

    def efetuarLogin(self):
        self.conectado, error = self.api.connect()
        if not self.conectado:
            logging.error(error)
            return False
        else:
            return True

    def checarAtivo(self, ativo):
        ativos = self.api.get_all_open_time()
        if ativos["digital"][ativo]["open"]:
            logging.info("Ativo encontrado")
            return True
        else:
            logging.error("O ativo {} nao foi encontrado".format(str(ativo)))
            print("O ativo {} nao foi encontrado".format(str(ativo)))
            return False

    def contaReal(self):
        self.api.change_balance("REAL")

    def contaDemo(self):
        self.api.change_balance("PRACTICE")

    def pegarSaldo(self):
        return self.api.get_balance()

    def pegarMoeda(self):
        return self.api.get_currency()

    def setDirecao(self, direcao):
        self.direcao = direcao

    def setEntrada(self, entrada):
        try:
            entrada = float(entrada)
        except:
            logging.error("Nao foi possivel definir o preco de entrada")
            return False
        if isinstance(entrada, float):
            self.entrada = entrada
            return True
        else:
            logging.error("Nao foi possivel definir o preco de entrada")
            return False

    def buy(self):
        if self.checarAtivo(self.ativo):
            try:
                logs.print_message(
                    "Executing programmed trade, paper:{}, action:{}, value:{}, exp:{}min".format(self.ativo,
                                                                                                  self.direcao,
                                                                                                  self.entrada,
                                                                                                  self.timeframe))
                _, order_id = self.api.buy(self.entrada, self.ativo, self.direcao, self.timeframe)
                result = self.api.check_win_v3(order_id)
                if result < 0:
                    logs.print_message(
                        "LOST: paper:{}, action:{}, value:{}".format(self.ativo, self.direcao, self.entrada))
                    logs.print_message("Initializing Martingale paper:{}, action:{}, value:{}".format(self.ativo,
                                                                                                      self.direcao,
                                                                                                      self.entrada))
                    gale_value = self.entrada * 2
                    logs.print_message(
                        "Executing programmed trade, paper:{}, action:{}, value:{}, exp:{}min".format(self.ativo,
                                                                                                      self.direcao,
                                                                                                      gale_value,
                                                                                                      self.timeframe))
                    _, gale_order_id = self.api.buy(gale_value, self.ativo, self.direcao, self.timeframe)
                    new_result = self.api.check_win_v3(gale_order_id)
                    if new_result < 0:
                        logs.print_message(
                            "LOST: paper:{}, action:{}, value:{}".format(self.ativo, self.direcao, self.entrada))
                    else:
                        logs.print_message(
                            "WIN: paper:{}, action:{}, value:{}".format(self.ativo, self.direcao, gale_value))
                else:
                    logs.print_message(
                        "WIN: paper:{}, action:{}, value:{}".format(self.ativo, self.direcao, self.entrada))
            except:
                import traceback
                logs.print_error("Error on execute order. paper:{}, action:{}, value:{}".format(self.ativo,
                                                                                                self.direcao,
                                                                                                self.entrada))
                logging.error(traceback.format_exc())
        logging.info("New balance: ${}".format(self.pegarSaldo()))
        schedule.CancelJob
        logs.print_message("Processing Orders...")
