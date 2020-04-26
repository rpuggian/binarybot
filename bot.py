import os
import datetime
import schedule
from logs import Logs
from iqoption import IQOption
from configs import Configuracoes
import csv
import threading
from iqoptionapi.stable_api import IQ_Option


logs = Logs()


def login(api):
    conectado, _ = api.connect()
    if not conectado:
        logs.print_error("Error on login.")
        return False
    else:
        return True


def add_option(ativo, startTime, direcao, entrada, stop_loss, api):
    configuracao = Configuracoes()
    configuracao.setAtivo(ativo)
    configuracao.setTimeframe(5)
    IQ = IQOption(api)
    IQ.setDirecao(direcao)
    IQ.definirConfiguracoes(configuracao.getAtivo(), configuracao.getTimeframe(), 1)
    IQ.contaReal()
    IQ.set_stop_loss(stop_loss)
    IQ.setEntrada(entrada)
    schedule.every().day.at(startTime).do(IQ.buy)
    logs.print_message("Trade programmed: paper:{}, exp:{}, action:{}, value:{} ✅".format(ativo, startTime, direcao, entrada))


def main():
    logs.print_message("Bot Started!")
    stop_loss = input("Set a stop loss value for today:")

    #login
    email = os.getenv('IQ_USER')
    password = os.getenv('IQ_PASS')
    api = IQ_Option(email, password)
    if not login(api):
        logs.print_error("Error on try to login. Check iq option credentials on environment variables.")
        input("Press any key to exit...")
        exit()

    #read trades
    f = open("trades.csv")
    csv_f = csv.reader(f)
    counter = 0
    for row in csv_f:
        if counter == 0:
            logs.print_message("Programming Orders...")
        else:
            start_time = datetime.datetime.strptime(row[1], '%H:%M')
            time_result = start_time - datetime.timedelta(seconds=6)
            add_option(row[0].replace('/', ''), time_result.strftime("%H:%M:%S"), row[2], row[3], stop_loss, api)
        counter = counter + 1

    logs.print_message("\nProcessing Orders...")

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()
