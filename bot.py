import os
import datetime
import schedule
from logs import Logs
from iqoption import IQOption
from configs import Configuracoes
import csv
import threading

logs = Logs()


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def add_option(ativo, startTime, direcao, entrada):
    # login
    email = os.getenv('IQ_USER')
    password = os.getenv('IQ_PASS')
    IQ = IQOption(email, password)
    login = IQ.efetuarLogin()
    if not login:
        logs.print_error("Error on try to login. Check iq option credentials on environment variables.")
        input("Press any key to exit...")
        exit()

    configuracao = Configuracoes()
    configuracao.setAtivo(ativo)
    configuracao.setTimeframe(5)
    IQ.setDirecao(direcao)
    IQ.definirConfiguracoes(configuracao.getAtivo(), configuracao.getTimeframe(), 1)
    IQ.contaReal()
    IQ.setEntrada(entrada)
    schedule.every().day.at(startTime).do(run_threaded, IQ.buy)
    logs.print_message("Trade Programado-->Ativo:{}, Entrada:{}, Action:{}, Valor:{} ✅".format(ativo, startTime, direcao, entrada))


def main():
    logs.print_message("Bot Started!")
    f = open("trades.csv")
    csv_f = csv.reader(f)
    counter = 0
    for row in csv_f:
        if counter == 0:
            logs.print_message("Programming Orders...")
        else:
            start_time = datetime.datetime.strptime(row[1], '%H:%M')
            time_result = start_time - datetime.timedelta(seconds=6)
            add_option(row[0].replace('/', ''), time_result.strftime("%H:%M:%S"), row[2], row[3])
        counter = counter + 1

    logs.print_message("Processing Orders...")

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()
