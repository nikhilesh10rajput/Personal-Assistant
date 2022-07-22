import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import base64


umailId="prufung101konto@gmail.com"
passwrd="Stellvertreter@101"
contctMailId="prufung101konto@gmail.com"
sbjct="test"
mssge="Heloo!"

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