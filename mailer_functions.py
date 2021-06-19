import mailersend
import os
from typing import List

os.environ["MAILERSEND_API_KEY"] = """eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNWNhMTY1Y2Q4NmIyYmRlNGYzZWY4NDllZTMyMmUwZGU5ZmY3OTRkMzRlMDE0ODBmOTQwYzVjNmM3NTZmMTE2N2RmNDA0NTk0Y2M5OWJkYzciLCJpYXQiOjE2MjQwODQ0OTYsIm5iZiI6MTYyNDA4NDQ5NiwiZXhwIjo0Nzc5NzU4MDk2LCJzdWIiOiI3NjgyIiwic2NvcGVzIjpbImVtYWlsX2Z1bGwiLCJkb21haW5zX2Z1bGwiLCJhY3Rpdml0eV9mdWxsIiwiYW5hbHl0aWNzX2Z1bGwiLCJ0b2tlbnNfZnVsbCIsIndlYmhvb2tzX2Z1bGwiLCJ0ZW1wbGF0ZXNfZnVsbCJdfQ.m_74bzxgAEO5g7S7qGuvH4JodfZSghDrBs6VSoB_hk9jvqNcLBQSx0F4v-_uuCr2Pg3Io9UaDws8yOI5aCqHa1IyQzWwUgXgthSBW5WmJ4lR9T8aMIMEoIbxaQd3NaWcJQlr6BpoEi_sxsIuEWkVvhKTmzZVjP8tVrDtopdklZay8ymJCx2Zx34AP-fkv3Q-qp2vSmBK9a8hoRRt7RaUo_mib-3ZbkzMtm5cpvPeyc7098_n4HznUPRxAp63rxdt-VFYjOOlyO2u713aLGeP-uqSqRz-73lZPnusk_yhVv5kiR76ozXLHubjSPorZEbGzsL7uiv2d-oYlfUd8-l4U0Udc6y-THEr8_lQktGLc62gpyjwaXe3PlnisYZDaaHx2hEkrbHhjpVbiBDqhZKXiTThhEoWMpxEsZfAUrZQeSwkevWeQah8kZ18JErFkOuf-tUgftH1VqpXzzusQcKE0VzfmbsGUykpx7ERg2l3aC588wzVhe4x0QkORUTnbDYdzadVtdYIafuDLIPWTnGkz5z3Oywe6myeGwZDGLB7lFNvgCDpr8On5ojVo4zh6y81Mxj4kN8jbsmmZmBuDKBjcpvgM5mgCTfR8hwp9-8Y3qLo8aZ3HxMSIucKU3C3C78FF9qIM-U8FTCZ1EFGJ8hHqC6UVI3ea8W0N7XZWgwV7Vg"""

mailer = mailersend.NewApiClient()

my_mail = "no-reply@mail.asap-it.tech"


def send_verification_link(verification_link: str, email: str):
    subject = "Verify your account"
    text = f"Click the link too verify your account: {verification_link}"
    print(mailer.send(my_mail, [email], subject, text))


def send_briefs(emails: List[str], briefes: str):
    subject = "Check our exciting news"
    print(mailer.send(my_mail, emails, subject, briefes))
