import time
import threading
from datetime import datetime
from flask import Flask, render_template
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

# Configurações de e-mail (SUBSTITUA COM SUAS CREDENCIAIS)
EMAIL_REMETENTE = "luiz.dev14@gmail.com"
EMAIL_SENHA = "oxoz plyg dqrd whlo"
EMAIL_DESTINATARIO = "cortexstudios24@gmail.com"

tempo_inicial = time.time()  # tempo_inicial agora será fixo, não será mais reiniciado
horas_totais = 0
ultima_log_50h = 0

@app.route("/")
def index():
    return render_template("index.html")

def enviar_email(caminho_arquivo):
    """Envia um e-mail com o arquivo de log em anexo."""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINATARIO
    msg['Subject'] = "Log de Manutenção - 500 Horas"

    with open(caminho_arquivo, "r") as arquivo:
        anexo = MIMEBase('application', "octet-stream")
        anexo.set_payload((arquivo).read())
        encoders.encode_base64(anexo)
        anexo.add_header('Content-Disposition', "attachment; filename= manutencao_500h.txt")
        msg.attach(anexo)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use o servidor SMTP do seu provedor
        server.starttls()
        server.login(EMAIL_REMETENTE, EMAIL_SENHA)
        server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
        server.quit()
        print("Email enviado com sucesso!")
        gerar_log("Email enviado com sucesso!", "importante")
    except Exception as e:
        print(f"Erro ao enviar o email: {e}")
        gerar_log(f"Erro ao enviar o email: {e}", "importante")

def gerar_log(mensagem, pasta="log"):
    """Gera um log da mensagem fornecida."""
    nome_arquivo = "contador.txt"
    if pasta == "importante":
        nome_arquivo = "manutencao_500h.txt"
    caminho_arquivo = os.path.join(pasta, nome_arquivo)
    mensagem_log = f"{datetime.now()} - {mensagem}\n"
    with open(caminho_arquivo, "a") as arquivo_log:
        arquivo_log.write(mensagem_log)
    print(mensagem_log.strip())

email_enviado = False  # Variável para controlar o envio do e-mail

def verificar_500_horas():
    global horas_totais, email_enviado

    # Verifica se o total de horas é múltiplo de 500 e se o e-mail não foi enviado ainda
    if horas_totais >= 500 and horas_totais % 500 == 0 and not email_enviado:
        gerar_log(f"Máquina chegou a {horas_totais} horas de uso, fazer manutenção!", "importante")
        caminho_arquivo_importante = os.path.join("importante", "manutencao_500h.txt")
        enviar_email(caminho_arquivo_importante)
        
        email_enviado = True  # Marca que o e-mail foi enviado

    # Se atingirmos um novo múltiplo de 500 horas, permite o envio de novos e-mails
    if horas_totais % 500 == 0 and horas_totais > 0:
        email_enviado = False

def loop_log():
    """Loop principal que monitora o tempo e gera os logs simulando o avanço do tempo."""

    global horas_totais
    global ultima_log_50h
    while True:
        time.sleep(3600)  # Agora o sleep é de 1 hora
        tempo_decorrido = int(time.time() - tempo_inicial)  # Calcula o tempo decorrido desde tempo_inicial
        horas = tempo_decorrido // 3600
        minutos = (tempo_decorrido % 3600) // 60
        segundos = tempo_decorrido % 60
        horas_totais += horas  # Incrementa as horas totais com o cálculo do tempo decorrido
        horas_desde_ultimo_log_50h = horas_totais - ultima_log_50h

        # Verifica se o log de 50 horas deve ser gerado
        if horas_desde_ultimo_log_50h >= 50:
            gerar_log(f"O contador está funcionando há {horas_totais:02} horas e está funcionando perfeitamente.")
            ultima_log_50h = horas_totais  # Atualiza a última hora de log de 50 horas

        # Verifica se atingiu múltiplos de 500 horas e envia o log por e-mail
        verificar_500_horas()

if __name__ == "__main__":
    os.makedirs("log", exist_ok=True)
    os.makedirs("importante", exist_ok=True)
    log_thread = threading.Thread(target=loop_log)
    log_thread.daemon = True
    log_thread.start()
    app.run(debug=True, host='0.0.0.0', port=5000)
import time
import threading
from datetime import datetime
from flask import Flask, render_template
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

# Configurações de e-mail (SUBSTITUA COM SUAS CREDENCIAIS)
EMAIL_REMETENTE = "luiz.dev14@gmail.com"
EMAIL_SENHA = "oxoz plyg dqrd whlo"
EMAIL_DESTINATARIO = "cortexstudios24@gmail.com"

tempo_inicial = time.time()  # tempo_inicial agora será fixo, não será mais reiniciado
horas_totais = 0
ultima_log_50h = 0

@app.route("/")
def index():
    return render_template("index.html")

def enviar_email(caminho_arquivo):
    # (Código de envio de e-mail permanece o mesmo)
    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINATARIO
    msg['Subject'] = "Log de Manutenção - 500 Horas"

    with open(caminho_arquivo, "r") as arquivo:
        anexo = MIMEBase('application', "octet-stream")
        anexo.set_payload((arquivo).read())
        encoders.encode_base64(anexo)
        anexo.add_header('Content-Disposition', "attachment; filename= manutencao_500h.txt")
        msg.attach(anexo)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use o servidor SMTP do seu provedor
        server.starttls()
        server.login(EMAIL_REMETENTE, EMAIL_SENHA)
        server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
        server.quit()
        print("Email enviado com sucesso!")
        gerar_log("Email enviado com sucesso!", "importante")
    except Exception as e:
        print(f"Erro ao enviar o email: {e}")
        gerar_log(f"Erro ao enviar o email: {e}", "importante")


def gerar_log(mensagem, pasta="log"):
    nome_arquivo = "contador.txt"
    if pasta == "importante":
        nome_arquivo = "manutencao_500h.txt"
    caminho_arquivo = os.path.join(pasta, nome_arquivo)
    mensagem_log = f"{datetime.now()} - {mensagem}\n"
    with open(caminho_arquivo, "a") as arquivo_log:
        arquivo_log.write(mensagem_log)
    print(mensagem_log.strip())


email_enviado = False  # Variável para controlar o envio do e-mail

def verificar_500_horas():
    global horas_totais, email_enviado

    if horas_totais >= 500 and not email_enviado:  # Verifica se 500 horas foram atingidas e se o email ainda não foi enviado
        gerar_log("Máquina chegou ao total de 500 horas de uso, fazer manutenção!", "importante")
        caminho_arquivo_importante = os.path.join("importante", "manutencao_500h.txt")
        enviar_email(caminho_arquivo_importante)
        
        email_enviado = True  # Marca que o e-mail foi enviado

        # NÃO RESETAMOS AS HORAS NEM O TEMPO INICIAL
        # O contador de horas continuará de onde parou, sem reiniciar

def loop_log():
    global horas_totais
    global ultima_log_50h
    while True:
        time.sleep(3600)  # Agora o sleep é de 1 hora
        tempo_decorrido = int(time.time() - tempo_inicial)  # Calcula o tempo decorrido desde tempo_inicial
        horas = tempo_decorrido // 3600
        minutos = (tempo_decorrido % 3600) // 60
        segundos = tempo_decorrido % 60
        horas_totais += horas  # Incrementa as horas totais com o cálculo do tempo decorrido
        horas_desde_ultimo_log_50h = horas_totais - ultima_log_50h
        if horas_desde_ultimo_log_50h >= 50:
            gerar_log(f"O contador está funcionando há {horas_totais:02} horas e está funcionando perfeitamente.")
            ultima_log_50h = horas_totais
        verificar_500_horas()

if __name__ == "__main__":
    os.makedirs("log", exist_ok=True)
    os.makedirs("importante", exist_ok=True)
    log_thread = threading.Thread(target=loop_log)
    log_thread.daemon = True
    log_thread.start()
    app.run(debug=True, host='0.0.0.0', port=5000)
