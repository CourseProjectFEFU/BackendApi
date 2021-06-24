from typing import List, Tuple
from smtplib import SMTP
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp = SMTP("mail.asap-it.tech", port=465)


def send_verification_link(verification_link: str, email: str, name: str):
    subject = "Verify your account"
    text = f"""From: ASAP NEWS <no-reply@mail.asap-it.tech>
To: {name}<{email}>
Subject: Подтвердите свой Email

Перейдите по ссылке для подтверждения почты: {verification_link}"""
    smtp.connect(host="151.248.123.101", port=465)
    print(smtp.sendmail("no-reply@mail.asap-it.tech", email, text.encode("utf-8")))
    smtp.close()


# subject = "Науменко - проректор по развитию"
# text = f"""From: ASAP NEWS<no-reply@asap-it.tech>
# To: TESTMAIL<enginer385@gmail.com>
# Subject: "email verification"
#
# Перейдите по ссылке для подтверждения почты /link/"""
#
# smtp.connect(host="151.248.123.101", port=465)
# print(smtp.sendmail("no-reply@mail.asap-it.tech", "enginer385@gmail.com", text.encode("utf-8")))
# smtp.close()

def send_briefs(emails: List[Tuple[str]], briefes: str):
    subject = "Наши офигенные новости"
    smtp.connect(host="151.248.123.101", port=465)
    for email_name in emails:
#         text = f"""From: ASAP NEWS<no-reply@mail.asap-it.tech>
# To: {email_name[1]}<{email_name[0]}>
# Content-Type: text/html
        text = f"""Посомтрите на наши очешуенные новости!
{briefes}
"""
        message = MIMEMultipart('alternative')
        message['Subject'] = 'New News'
        message['From'] = 'no-reply@mail.asap-it.tech'
        message['To'] = email_name[0]
        message.attach(MIMEText(text, 'html'))
        message.attach(MIMEText(text, 'plain'))
        print(message.as_string())
        smtp.sendmail("no-reply@mail.asap-it.tech", [email_name[0]], message.as_string())
    smtp.close()
