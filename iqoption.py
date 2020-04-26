import schedule
import logging
from logs import Logs

logs = Logs()


class IQOption:
    def __init__(self, api):
        super().__init__()
        self.api = api

    def definirConfiguracoes(self, ativo, timeframe, posicao):
        self.ativo = ativo
        self.timeframe = int(timeframe)
        self.posicao = int(posicao)

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

    def set_original_balance(self, balance):
        self.original_balance = balance

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
        
    def set_stop_win(self, stop_win):
        try:
            stop_win = float(stop_win)
        except:
            logging.error("Nao foi possivel definir o preco de stop_win")
            return False
        if isinstance(stop_win, float):
            self.stop_win = stop_win
            return True
        else:
            logging.error("Nao foi possivel definir o preco de stop_win")
            return False
    
    def set_stop_loss(self, stop_loss):
        try:
            stop_loss = float(stop_loss)
        except:
            logging.error("Nao foi possivel definir o preco de stop_loss")
            return False
        if isinstance(stop_loss, float):
            self.stop_loss = stop_loss
            return True
        else:
            logging.error("Nao foi possivel definir o preco de stop_loss")
            return False
    
    def check_trade_result(self, order_id):
        result = self.api.check_win_v3(order_id)
        if result < 0:
             logs.print_message(
                        "LOST: paper:{}, action:{}, value:{} ❌".format(self.ativo, self.direcao, self.entrada))
        else:
            logs.print_message(
                            "WIN: paper:{}, action:{}, value:{} ✅".format(self.ativo, self.direcao, self.entrada))
        return result


    def execute_martingale(self):
        self.entrada = self.entrada * 2
        logs.print_message("Initializing Martingale paper:{}, action:{}, value:{}".format(self.ativo,
                                                                                          self.direcao,
                                                                                          self.entrada))
       
        logs.print_message(
            "Executing programmed trade, paper:{}, action:{}, value:{}, exp:{}min".format(self.ativo,
                                                                                          self.direcao,
                                                                                          self.entrada,
                                                                                          self.timeframe))
        _, gale_order_id = self.api.buy( self.entrada, self.ativo, self.direcao, self.timeframe)
        result = self.check_trade_result(gale_order_id)
        if result < 0:
            self.entrada = self.entrada * 2
            logs.print_message("Initializing Martingale 2 paper:{}, action:{}, value:{}".format(self.ativo,
                                                                                            self.direcao,
                                                                                            self.entrada))
        
            logs.print_message(
                "Executing programmed trade mg2, paper:{}, action:{}, value:{}, exp:{}min".format(self.ativo,
                                                                                            self.direcao,
                                                                                            self.entrada,
                                                                                            self.timeframe))
            _, gale2_order_id = self.api.buy( self.entrada, self.ativo, self.direcao, self.timeframe)
            self.check_trade_result(gale2_order_id)

    
    def buy(self):
        balance = self.pegarSaldo()
        if balance <= self.stop_loss:
            logs.print_message("Stop loss reached, no trading more today. ❌")
            exit()

        if self.checarAtivo(self.ativo):
            try:
                logs.print_message(
                    "Executing programmed trade, paper:{}, action:{}, value:{}, exp:{}min".format(self.ativo,
                                                                                                  self.direcao,
                                                                                                  self.entrada,
                                                                                                  self.timeframe))
                _, order_id = self.api.buy(self.entrada, self.ativo, self.direcao, self.timeframe)
                result = self.check_trade_result(order_id)
                if result < 0:
                    self.execute_martingale()
                    
            except:
                import traceback
                logs.print_error("Error on execute order. paper:{}, action:{}, value:{}".format(self.ativo,
                                                                                                self.direcao,
                                                                                                self.entrada))
                logging.error(traceback.format_exc())
        logs.print_message("New balance: ${}".format(self.pegarSaldo()))
        schedule.CancelJob
        logs.print_message("\nProcessing Orders...")
