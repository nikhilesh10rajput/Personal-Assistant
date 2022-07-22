import smtplib
import ssl
import imaplib
import email
import datetime
import tkinter


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing_extensions import ParamSpecKwargs
from threading import Thread

umailId="prufung101konto@gmail.com"
passwrd="Stellvertreter@101"
contctMailId="prufung101konto@gmail.com"
sbjct="test"
mssge="Heloo!"

msg=MIMEMultipart()
msg['From']=umailId
msg['To']=contctMailId
msg['Subject']=sbjct
message=mssge
msg.attach(MIMEText(message))

mailserver=smtplib.SMTP('smtp.gmail.com',587)
mailserver.ehlo()
mailserver.starttls(context=ssl.create_default_context()) # Secure the connection
mailserver.ehlo()
mailserver.login(umailId,passwrd)
mailserver.sendmail(umailId,contctMailId,msg.as_string())
mailserver.quit()