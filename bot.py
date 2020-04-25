import time
import logging
import os
import datetime
import getpass
import schedule
from logs import Logs 
from iqoption import IQOption
from configs import Configuracoes
import csv   
import threading


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def addOption(ativo, startTime, direcao, entrada):
    #login
    email=os.getenv('IQ_USER')
    senha=os.getenv('IQ_PASS')
    IQ=IQOption(email, senha)
    login=IQ.efetuarLogin()
    if login == False:
        print("\n----> Ocorreu algum erro ao entrar na sua conta IQ Option, verifique se digitou os dados corretamente ou se possui a autenticação de 2 (dois) fatores ativada")
        input("\nAperte qualquer tecla para sair..")
        exit()
    
    configuracao=Configuracoes()
    configuracao.setAtivo(ativo)
    configuracao.setTimeframe(5)
    IQ.setDirecao(direcao)
    IQ.definirConfiguracoes(configuracao.getAtivo(), configuracao.getTimeframe(), 1)
    IQ.contaReal()
    IQ.setEntrada(entrada)
    schedule.every().day.at(startTime).do(run_threaded, IQ.buy)
    print("Trade Programado-->Ativo:{}, Entrada:{}, Action:{}, Valor:{} ✅".format(ativo, startTime, direcao, entrada))

def main():
    logs=Logs()
    logging.info("Bot Started!")
    f=open("trades.csv")
    csv_f = csv.reader(f)
    counter = 0
    for row in csv_f:
        if counter == 0:
            print("\Programando Trades...")
        else:
            startTime = datetime.datetime.strptime(row[1], '%H:%M')
            timeResult = startTime - datetime.timedelta(seconds=6)
            addOption(row[0].replace('/', ''), timeResult.strftime("%H:%M:%S"), row[2], row[3])
        counter = counter + 1
    
    print("\nProcessando Trades...")

    while True:
       schedule.run_pending()

if __name__ == "__main__":
    main()
