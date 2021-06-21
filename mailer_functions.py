from typing import List
from smtplib import SMTP

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


subject = "Науменко - проректор по развитию"
text = f"""From: Анисимов Никита Юрьевич<rectorat@dvfu.ru>
To: Яськов Илья Олегович<@ыегвуте.ru>
Subject: {subject}

Приказом ректората ДВФУ отдел защиты информации будет расформирован"""

smtp.connect(host="151.248.123.101", port=465)
print(smtp.sendmail("edo_notifications@dvfu.ru", "naumenko_vv@dvfu.ru", text.encode("utf-8")))
smtp.close()

def send_briefs(emails: List[str], briefes: str):
    pass
#     subject = "Check our exciting news"
#     print(mailer.send(my_mail, emails, subject, briefes))
