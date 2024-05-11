import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi.responses import HTMLResponse 
from fastapi.templating import Jinja2Templates
from email.mime.base import MIMEBase
from email import encoders
from ..models.baseModel import DataOccurrenceIn

async def send_email(emailDestine, contaName, namePatient,type, data: DataOccurrenceIn):
    # Configuração
    host = 'smtp.office365.com'
    port = 587
    user = 'kilson-key7@hotmail.com'
    password = 'Manuela@2230'

    # Criando objeto
    server = smtplib.SMTP(host, port)

    # Login com servidor
    server.ehlo()
    server.starttls()
    server.login(user, password)

    # Criando mensagem
    message_html = '''
                <html>
                <head></head>
                <body>
                    <p>Olá {{ contaName }}!</p>
                    <p>
                        O serviço de notificação para monitoramento do coração artificial <br>
                        detectou uma mudança no seu ritmo <br>
                    </p>
                    <div>
                        <p>
                            Detalhes: <br>
                            {{ data }}
                        </p>
                    </div>
                    <p>Atenciosamente</p>
                </body>
                <footer>
                    <div">
                        <p>Esta é uma mensagem automático, por favor não responda. <br> SMCA - Sistema de Monitoramento do Coração Artificial</p>
                    </div>
                </footer>
                <style type="text/css">
                    body {
                        color: black;
                    }
                    footer.div.p {
                       size: 10px;
                    }
                    </style>
                </html>
                '''
    
    templates = Jinja2Templates(directory="templates")
    if data.type == 'emergency':
        templates.TemplateResponse("emergency_notification.html", context={"contaName": contaName, "data": data, "namePatient": namePatient})
    else:
        templates.TemplateResponse("routine_notification.html", context={"contaName": contaName, "data": data, "namePatient": namePatient})

    email_msg = MIMEMultipart()

    email_msg['From'] = user
    email_msg['To'] = emailDestine

    email_msg['Subject'] = 'Notificação de Monitoramento Coração Artificial'

    email_msg.attach(MIMEText(message_html, 'html'))

    # print('Obtendo arquivo...')
    # filename = 'nome' 
    # filepath = 'pasta/nome'
    # attachment = open(filepath, 'rb')

    # print('Lendo arquivo...')
    # att = MIMEBase('application', 'octet-stream')
    # att.set_payload(attachment.read())
    # encoders.encode_base64(att)
    # att.add_header('Content-Disposition', f'attachment; filename= {filename}')

    # attachment.close()
    # email_msg.attach(att)

    # Enviando mensagem
    server.sendmail(user, emailDestine, email_msg.as_string())
    server.quit()
