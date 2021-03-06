import os
import datetime
import schedule
from logs import Logs
from iqoption import IQOption
from configs import Configuracoes
import csv
import threading
from iqoptionapi.stable_api import IQ_Option
import time
import threading


logs = Logs()


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def login(api):
    conectado, _ = api.connect()
    if not conectado:
        logs.print_error("Error on login.")
        return False
    else:
        return True


def add_option(ativo, startTime, direcao, entrada, stop_loss, stop_win, api, original_balance):
    configuracao = Configuracoes()
    configuracao.setAtivo(ativo)
    configuracao.setTimeframe(5)
    IQ = IQOption(api)
    IQ.setDirecao(direcao)
    IQ.definirConfiguracoes(configuracao.getAtivo(), configuracao.getTimeframe(), 1)
    IQ.set_original_balance(original_balance)
    IQ.set_stop_win(stop_win)
    IQ.set_stop_loss(stop_loss)
    IQ.setEntrada(entrada)
    schedule.every().day.at(startTime).do(run_threaded, IQ.buy)
    logs.print_message("Trade programmed: paper:{}, exp:{}, action:{}, value:{} ✅".format(ativo, startTime, direcao, entrada))


def main():
    logs.print_message("Bot Started!")

    #login
    logs.print_message("Login Credentials IQ Option:")
    email = input("Email:")
    password = input("Pass:")
    api = IQ_Option(email, password)
    if not login(api):
        logs.print_error("Error on try to login. Check iq option credentials on environment variables.")
        exit()
    logs.print_message("Conected: IQ Option!")

    #stops
    #REAL / PRACTICE
    account_type = input("Set the account type (REAL or PRACTICE):")
    api.change_balance(account_type)
    original_balance = api.get_balance()
    logs.print_message("Original balance: $ {}".format(original_balance))
    stop_loss = input("Set a stop loss value:")
    stop_win = input("Set a stop win value:")

    #read trades
    f = open("trades.csv")
    csv_f = csv.reader(f)
    counter = 0
    for row in csv_f:
        if counter == 0:
            logs.print_message("Programming Orders...")
        else:
            start_time = datetime.datetime.strptime(row[1], '%H:%M')
            time_result = start_time - datetime.timedelta(seconds=15)
            add_option(row[0].replace('/', ''), time_result.strftime("%H:%M:%S"), row[2], row[3], stop_loss, stop_win, api, original_balance)
        counter = counter + 1

    logs.print_message("\nProcessing Orders...")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
