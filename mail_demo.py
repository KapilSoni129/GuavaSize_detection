import smtplib
import os
import imghdr
from email.message import EmailMessage

EMAIL_ADDRESS = 'priyanshusoni005@gmail.com'
EMAIL_PASSWORD = 'kdlhniwgrhicwuqg'

msg = EmailMessage()
msg['Subject'] = 'Guava detected'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'sahiln21102@iiitnr.edu.in'
msg.set_content('A Guava has been detected in the tree , size will be mailed to you later')

smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)




def send_mail(file,coord):
    msg.set_content(str(coord))
    with open(file, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name

    msg.add_attachment(file_data, maintype='image', subtype =file_type, filename=file_name)
    smtp.send_message(msg)

    # with smtplib.SMTP('localhost', 1025) as smtp:
    # with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    #     smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    #     smtp.send_message(msg)

def send_mail2(ciord):
    msg.set_content(str(ciord))
    smtp.send_message(msg)

def disconnect_server():
    smtp.quit()
    





