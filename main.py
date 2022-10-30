# Importando bibliotecas
import requests
import time
import telebot
from datetime import datetime

key = '5427068016:AAFbIAjMiG8uHKxW3Ee5-ZUXuvsOSGcI0Mo'

bot = telebot.TeleBot(key)

# Segundo turno
url = "https://resultados.tse.jus.br/oficial/ele2022/545/dados-simplificados/br/br-c0001-e000545-r.json"

print('Rodando bot de apuração - ApuRamalas')


def polling():
    try:
        bot.polling()
    except:
        print("ConnectionError - Sending again after 5 seconds!!!")
        time.sleep(5)
        bot.polling()


@bot.message_handler(commands=["votos"])
def votos(mensagem):
    text = ""
    resp = requests.get(url)
    resp = resp.json()
    today = datetime.today()
    candidatos = resp['cand']
    text += f"\n TOTAL DE URNAS APURADAS - {resp['pst']}% às {today.strftime('%H:%M')} \n\n"
    for candidato in candidatos:
        text += str(candidato['nm'] + ' - ' + candidato['pvap'] + "% - " + candidato['vap'] + ' votos totais\n\n')
    bot.send_message(mensagem.chat.id, text)


def verificar(mensagem):
    return True


@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """
    Escolha uma opção para continuar (Clique no item):
     /votos Checar as porcentagens
Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto)


polling()
