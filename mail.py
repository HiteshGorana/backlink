import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
USERNAME = 'info.opositive@gmail.com'
PASSWORD = 'Obbserv@123'
# RECIEVER_EMAIL = 'to.hitesh.gorana@gmail.com'


def send_email(filename, RECIEVER_EMAIL):
    subject = 'Backlink tool'
    bodyText = """\
    Hi,
    by Obbserv
    """
    message = MIMEMultipart()
    message["From"] = USERNAME
    message["To"] = RECIEVER_EMAIL
    message["Subject"] = subject

    message.attach(MIMEText(bodyText, 'plain'))
    attachment = open(filename, "rb")

    mimeBase = MIMEBase('application', 'octet-stream')
    mimeBase.set_payload(attachment.read())

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
