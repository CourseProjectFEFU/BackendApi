from typing import List, Tuple
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp = SMTP("mail.asap-it.tech", port=465)


def send_verification_link(verification_link: str, email: str, name: str):
    text = f"""From: ASAP NEWS <no-reply@mail.asap-it.tech>
To: {name}<{email}>
Subject: Подтвердите свой Email

Перейдите по ссылке для подтверждения почты: {verification_link}"""
    smtp.connect(host="151.248.123.101", port=465)
    print(smtp.sendmail("no-reply@mail.asap-it.tech", email, text.encode("utf-8")))
    smtp.close()


# subject = "Науменко - проректор по развитию"
# text = f"""From: ASAP NEWS<no-reply@asap-it.tech>
# To: TEST MAIL<enginer385@gmail.com>
# Subject: "email verification"
#
# Перейдите по ссылке для подтверждения почты /link/"""
#
# smtp.connect(host="151.248.123.101", port=465)
# print(smtp.sendmail("no-reply@mail.asap-it.tech", "enginer385@gmail.com", text.encode("utf-8")))
# smtp.close()


def send_briefs(emails: List[Tuple[str, str]], briefes: str):
    smtp.connect(host="151.248.123.101", port=465)
    for email_name in emails:
        text = f"""Посомтрите на наши очешуенные новости!<br/>
{briefes}
"""
        message = MIMEMultipart("alternative")
        message["Subject"] = "New News"
        message["From"] = "no-reply@mail.asap-it.tech"
        message["To"] = email_name[0]
        message.attach(MIMEText(text, "html"))
        print(message.as_string())
        smtp.sendmail(
            "no-reply@mail.asap-it.tech", [email_name[0]], message.as_string()
        )
    smtp.close()
