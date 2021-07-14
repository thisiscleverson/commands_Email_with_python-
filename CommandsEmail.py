#----------------------[bibliotecas]-------------------------#
import email
import imaplib

import smtplib
from email.mime.text import MIMEText

#----------------------[dados do email]----------------------#
username = 'youremail@gmail.com'                       # email
password = 'yourpassword'                                   # senha 
server = 'imap.gmail.com'                                 # servidor do email >no caso é gmail.com >
admin = '"name admin" <adiminExemplo@gmail.com>'   # adimin do bot

#----------------------[variaveis globais]--------------------# 
global name_bot; name_bot = "name of bot"   # nome do bot [o nome tem que ser tudo em maiúscula!]
global data; data = None             # dados para o comandos
global attentive; attentive = False  # modo para ficar atento

#----------------------[funções]--------------------# 

def read_email(): # função para ler os email
    
    mail = imaplib.IMAP4_SSL(server)
    mail.login(username, password) # fazer o login no email

    mail.select("inbox")

    status,data = mail.search(None,'UNSEEN') #--> (UNSEEN) é para ler os email recentes! Para ler todos os email é só trocar '(UNSEEN)' para 'ALL'
    mail_ids = []

    for block in data:
        mail_ids += block.split()

    for i in mail_ids:
        status,data = mail.fetch(i,'(RFC822)')

        for response_part in data:

            if isinstance(response_part,tuple):
                message = email.message_from_bytes(response_part[1])
                mail_from = message['from']
                mail_subject = message['subject']

                if message.is_multipart():
                    mail_content = ''

                    for part in message.get_payload():  
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()
                
                bot_commands(mail_from, mail_subject)


def bot_commands(emailFrom, emailSubject): #comandos para o bot
    
    global data         # dados para os comandos
    global attentive   # modo para ficar atento
    global name_bot   # nome do bot 

    commands = emailSubject.upper() # mudar para maiúscula

    if emailFrom == admin: #veficar se a mensagem enviada foi do admin

        if commands == name_bot: #nome do bot
            attentive = True  # valor para o bot ficar atento quando for chamado!


        if attentive == True: # valor para o bot ficar atento quando for chamado!
            
            #comandos do bot
            if commands == 'ACENDER LUZ' or commands == 'LUZ ON': # LIGAR LUZ
                print("comando1") # COMANDO 1
            elif commands == "DESLIGAR LUZ" or commands == "LUZ OFF": # DESLIGAR LUZ
                print("comando1") # COMANDO 2
            elif commands == "LIGAR TOMADA" or commands == "TOMADA ON": # LIGAR TOMADA
                print("comando2") # COMANDO 3
            elif commands == "DESLIGAR TOMADA" or commands == "TOMADA OFF": # DESLIGAR TOMADA
                print("comando3") # COMANDO 4
            elif commands == "LIGAR DESPERTADOR" or commands == "DESPERTADOR ON": # LIGAR DESPERTADOR
                print("comando4") # COMANDO 5
            elif commands == "DESLIGAR DESPERTADOR" or commands == "DESPERTADOR OFF": # DESLIGAR DESPERTADOR
                print("comando5") # COMANDO 6
            elif commands == "LIGAR DISPLAY" or commands == "DISPLAY ON": # LIGAR DISPLAY
                print("comando6") # COMANDO 7
            elif commands == "DESLIGAR DISPLAY" or commands == "DESPERTADOR OFF": # DESLIGAR DISPLAY
                print("comando7") # COMANDO 8
            elif commands == "LIGAR BUZER" or commands == "BUZER ON": # LIGAR BUZER
                print("comando8") # COMANDO 9
            elif commands == "DESLIGAR BUZER" or commands == "BUZER OFF": # DESLIGAR BUZER
                print("comando9") # COMANDO 10
            elif commands == "DESLIGAR RASPI" or commands == "SHUTDOWN NOW": # DESLIGAR RASPBERRY 
                print("comando10") # COMANDO 11
            elif commands == "REINICIAR" or commands == "REBOOT": # DESLIGAR RASPBERRY 
                print("comando11") # COMANDO 12
            elif commands == "HELP":
                try:
                    msg = """
                    -------------------------------[comandos]----------------------------
                     Comandos para que pode ser execultado:

                    --> "luz on" para ligar a Luz;
                    --> "luz off" para desligar a luz;
                    --> "tomada on" para ativar a tomada;
                    --> "luz off" para desativar a tmada;
                    --> "despertador on" para ativar o despertador;
                    --> "despertador off" para desativar o despertador;
                    --> "display on" para ativar o display;
                    --> "display off" para desativar o display;
                    --> "buzer on" para ativar o buzer;
                    --> "buzer off" para desativar o buzer;
                    --> "shutdown now" ou "desligar raspi" para desligar o raspberry;
                    --> "reboot" ou "reiniciar" para fazer o reboot no raspberry;
                    -----------------------------------------------------------------------
                    """
                    sends_mail(msg)
                except:
                    pass


            elif commands == name_bot:
                print("sara foi chamada!")
                try:
                    msg = """Estou aqui! Como posso ajudar? \nvocê pode digitar "help" para listar comandos!"""
                    sends_mail(msg) #enviar mensagem por email de confirmação
                except:
                    print ("erro a enviar a mensagem!")

            else: 
                print("comando desconhecido!{}".format(commands))

    else:# mostrar que uma pessoa desconhecia mandou mensagem para o bot
        print("pessoa desconhecida!")
    

def sends_mail(sends): # função para enviar mensagem

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465) # iniciar conexão com servidor

    server.login(username, password) # fazer login 
    to_addrs = ['to_whom_to_send@gmail.com'] #para quem vai ser enviado o email

    message = MIMEText(sends)
    message['subject'] = "name" # a mensagem que vai ser enviada
    message['from'] = username # email da pessoa que vai enviar a mensagem
    message['to'] = ', '.join(to_addrs)  #para quem vai ser enviado o email

    server.sendmail(username, to_addrs, message.as_string()) # modolo que envia a mensagem
    server.quit() # sair do sevidor


def start_bot(sends): # função para iniciar o bot 

    if sends != None:
        try:
            sends_mail(sends)
        except:
            print("erro!")
    
    # tratamento de erros
    try: 
        read_email()
    except:
        print("Erro na conexão", end="")
