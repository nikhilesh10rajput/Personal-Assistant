import smtplib
import imaplib
import email
import datetime
import tkinter

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing_extensions import ParamSpecKwargs
from threading import Thread

reminderList=[]
umailId="prufung101konto@gmail.com"
passwrd="Stellvertreter@101"
contctMailId="prufung101konto@gmail.com"
sbjct="Test email (sent)"
mssge="Hello Google!"

sendEmail(umailId,passwrd,contctMailId,sbjct,mssge):
msg=MIMEMultipart()
msg['From']=umailId
msg['To']=contctMailId
msg['Subject']=sbjct
message=mssge
msg.attach(MIMEText(message))

mailserver=smtplib.SMTP('smtp.gmail.com',587)
mailserver.ehlo()
mailserver.login(umailId,passwrd)
mailserver.sendmail(umailId,contctMailId,msg.as_string())
mailserver.quit()

sendEmail(umailId,passwrd,contctMailId,sbjct,mssge)