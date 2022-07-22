import smtplib
import ssl
import imaplib
import email
from email.header import decode_header
import datetime
import tkinter

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing_extensions import ParamSpecKwargs
from threading import Thread

toDoArr=[]      #Stores all "To-Dos" in string form

def sendEmail(umailId,passwrd,contctMailId,sbjct,mssge):
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

def readEmail(umailId,passwrd):
    mail=imaplib.IMAP4_SSL('imap.gmail.com', 993)
    mail.login(umailId,passwrd)
    mail.select("INBOX")

    _, message_numbers_raw = mail.search(None, 'ALL')
    for message_number in message_numbers_raw[0].split():
        _, msg = mail.fetch(message_number, '(RFC822)')
        message = email.message_from_bytes(msg[0][1])
        print("Ref. No.: "+str(message_number)+" ")
        print(f'From: {message["from"]}')
        print(f'Subject: {message["subject"]}')
        print("\n")

    RefNo=str(input("Enter reference number"))
    for message_number in message_numbers_raw[0].split():
        if(RefNo==str(message_number)):
            _, msg = mail.fetch(message_number, '(RFC822)')

            # Parse the raw email message in to a convenient object
            message = email.message_from_bytes(msg[0][1])
            print('== Email message =====')
            # print(message)  # print FULL message
            print('== Email details =====')
            print(f'From: {message["from"]}')
            print(f'To: {message["to"]}')
            print(f'Cc: {message["cc"]}')
            print(f'Bcc: {message["bcc"]}')
            print(f'Subject: {message["subject"]}')
            print(f'Urgency (1 highest 5 lowest): {message["x-priority"]}')
            print(f'Object type: {type(message)}')
            print(f'Content type: {message.get_content_type()}')
            print(f'Content disposition: {message.get_content_disposition()}')
            print(f'Multipart?: {message.is_multipart()}')
            # If the message is multipart, it basically has multiple emails inside
            # so you must extract each "submail" separately.
            if message.is_multipart():
                print('Multipart types:')
                for part in message.walk():
                    print(f'- {part.get_content_type()}')
                multipart_payload = message.get_payload()
                for sub_message in multipart_payload:
                    # The actual text/HTML email contents, or attachment data
                    print(f'Payload\n{sub_message.get_payload()}')
            else:  # Not a multipart message, payload is simple string
                print(f'Payload\n{message.get_payload()}')
        else:
            pass

def writeNotes(note):
    wr=str(input("Enter note title (enter extensions, too) \n"))
    wNotes=open(wr,"w")
    wNotes.write(note)
    wNotes.close()

def readNotes():
    rd=str(input("Enter title of note to be read (enter extensions, too)\n"))
    rNotes=open(rd,"r")
    print(rNotes.readlines())
    rNotes.close()

class reminders:
    def __init__(self,day,month,year,hour,min,stat):
        self.day=day
        self.month=month
        self.year=year
        self.hour=hour
        self.min=min
        self.stat=stat


def checkReminder(g):
    dt=datetime.datetime.now()

    if(g.day==dt.day)and(g.month==dt.month)and(g.year==dt.year)and(g.hour==dt.hour)and(g.min==dt.minute):
        return True


reminderList=[]

def main_function():
    while(True):
        print('''Hi! How can I help you?
                [mails  notes&to-do   reminder] \n''')
        x=str(input())

        if(x=="mails"):
            umailId=str(input("Enter YOUR email Id \n"))
            passwrd=str(input("Enter password \n"))
            contctMailId=str(input("Enter reciever's email Id \n"))

            print('''Do you want to
                    <send> or <read> mails? \n''')
            mail=str(input())

            if(mail=="send"):
                sbjct=str(input("Enter Subject"))
                salutation=str(input("Salutation \n"))
                body=str(input("Write body \n"))
                signature=str(input("Signature \n"))
                name=str(input("Enter your name \n"))

                message=salutation+"\n"+body+"\n"+"\n"+signature+"\n"+name

                sendEmail(umailId,passwrd,contctMailId,sbjct,message)


            elif(mail=="read"):
                readEmail(umailId,passwrd)


        elif(x=="notes&to-do"):
            print('''Do you want to edit
                    <notes> or <to-do>? \n''')
            nt=str(input())

            if(nt=="notes"):
                print('''Do you want to
                        <write> or <read> notes? \n''')
                notes=str(input())

                if(notes=="write"):
                    inpt=str(input("Write the note\n"))
                    writeNotes(inpt)
                    
                elif(notes=="read"):
                    readNotes()


            elif(nt=="to-do"):
                print('''Do you want to 
                        <add>, <delete>, <view>? \n''')
                todo=str(input())

                if(todo=="add"):
                    add=str(input("Enter your input \n"))
                    toDoArr.append(add)
                
                elif(todo=="delete"):
                    dele=str(input("Enter serial number"))
                    if((dele < len(toDoArr))and(dele>0)):
                        toDoArr.pop(dele-1)

                elif(todo=="view"):
                    print("To-Do List: \n")
                    print(toDoArr)

            

        elif(x=="reminder"):

            reminder=str(input("What to remind? \n"))
            day=int(input("Enter day \n"))
            month=int(input("Enter month (numerical input expected) \n"))
            year=int(input("Enter year \n"))
            hour=int(input("Time to remind (hour) \n"))
            min=int(input("Time to remind (minute) \n"))
            
            current_reminder=reminders(day,month,year,hour,min,reminder)

            reminderList.append(current_reminder)





def callReminder():
    while(True):
        for i in range(0,len(reminderList)):
            if(checkReminder(reminderList[i])==True):
                window=tkinter.Tk()
                window.geometry("500x300")
                window.title("REMINDER!!!")
                textt="Remember to \n"+reminderList[i].stat
                li=tkinter.Label(window, text=textt, font=('Comic Sans MS',32,'bold italic')).place(x=10,y=80)

                def clicked():
                    reminderList.pop(i)
                    window.destroy()
                bt=tkinter.Button(window,text="OK",command=clicked).place(x=250,y=200)
                window.mainloop()
            else:
                pass

Thread(target=callReminder).start()
Thread(target=main_function).start()
