from iqoptionapi.stable_api import IQ_Option
import schedule
import logging
import functools

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
        self.conectado, erro = self.api.connect()
        if self.conectado == False:
            logging.error(
                "Erro ao tentar entrar na conta IQ Option -> {}".format(str(erro)))
            return False
        else:
            logging.info("Sucesso ao entrar na conta IQ Option")
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
        if self.checarAtivo(self.ativo) :
            try:
                print("---> Fazendo Trade, Ativo:{}, Valor:{}, EXP:{}min".format(self.ativo, self.entrada, self.timeframe))
                _, ordem_id = self.api.buy(self.entrada, self.ativo, self.direcao, self.timeframe)
                result = self.api.check_win_v3(ordem_id)
                if result < 0:
                
                    print("---> Você perdeu: Ativo:{}, Valor:{}, Result:LOSE".format(self.ativo, self.entrada))
                    print("---> Tentando Martin Gale...")
                    newValue = self.entrada*2
                    print("---> Fazendo Trade, Ativo:{}, Valor:{}, EXP:{}min".format(self.ativo, newValue, self.timeframe))
                    _, newordem_id = self.api.buy(newValue, self.ativo, self.direcao, self.timeframe)
                    newResult = self.api.check_win_v3(newordem_id)
                    if newResult < 0:
                        logging.info("Ativo:{}, Valor:{}, Result:LOSE".format(self.ativo, newValue))
                    else: 
                        logging.info("Ativo:{}, Valor:{}, Result:WIN".format(self.ativo, newValue))
                        print("---> Você ganhou.")
                else: 
                    logging.info("Ativo:{}, Valor:{}, Result:WIN".format(self.ativo, self.entrada))
                    print("---> Você ganhou.")
            except:
                import traceback
                print("Error ao executar o trade.")
                logging.error("Error ao executar trade.")
                logging.error(traceback.format_exc())
        schedule.CancelJob
        print("\nProcessando...")

    