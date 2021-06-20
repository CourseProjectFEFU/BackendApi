from typing import List
from smtplib import SMTP

smtp = SMTP("mail.asap-it.tech", port=465)

def send_verification_link(verification_link: str, email: str, name: str):
    subject = "Verify your account"
    text = f"""From: ASAP NEWS <no-reply@mail.asap-it.tech>
To: {name}<{email}>
Subject: Подтвердите свой Email

Перейдите по ссылке для подтверждения почты: {verification_link}"""
    print(smtp.sendmail("no-reply@mail.asap-it.tech", email, text.encode("utf-8")))


# def send_briefs(emails: List[str], briefes: str):
#     subject = "Check our exciting news"
#     print(mailer.send(my_mail, emails, subject, briefes))
