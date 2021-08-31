import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

USERNAME = 'info.opositive@gmail.com'
PASSWORD = 'Obbserv@123'


def send_email(data, filename, RECIEVER_EMAIL, bodyText):
    subject = 'Backlink tool'
    message = MIMEMultipart()
    message["From"] = USERNAME
    message["To"] = RECIEVER_EMAIL
    message["Subject"] = subject

    message.attach(MIMEText(bodyText, 'plain'))
    attachment = data

    mimeBase = MIMEBase('application', 'octet-stream')
    mimeBase.set_payload(attachment)

    encoders.encode_base64(mimeBase)
    mimeBase.add_header('Content-Disposition', "attachment; filename= " + filename)

    message.attach(mimeBase)
    text = message.as_string()

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()

    session.login(USERNAME, PASSWORD)
    session.sendmail(USERNAME, RECIEVER_EMAIL, text)
    session.quit()
    return True
