import smtplib
import ssl
from email.message import EmailMessage
from celery import Celery
from config import SMTP_USER, SMTP_PASSWORD, REDIS_HOST, REDIS_PORT

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587

celery = Celery('tasks', broker=f"redis://{REDIS_HOST}:{REDIS_PORT}")


# def get_email_template_msg(username: str):
#     email = EmailMessage()
#     email['Subject'] = f'Welcome {username}'
#     email['From'] = "rasulabduvaitov@gmail.com"
#     email['To'] = username
#
#     email.set_content(
#         f"""
#     <h1>Welcome {username}</h1>
#     <p>You have been successfully registered.</p>
#     """,
#         subtype="html",
#     )
#
#     return email
#
#
# @celery.task
# def send_email(username: str):
#     email = get_email_template_msg(username)
#     with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
#         server.starttls()
#         server.login(SMTP_USER, SMTP_PASSWORD)
#         server.send_message(email)


port = 587  # For starttls
smtp_server = "smtp.gmail.com"
receiver_email = "forrasul003@gmail.com"
password = SMTP_PASSWORD
message = """\
Subject: Hi there

This message is sent from Python."""


@celery.task
def send_email_v2(user_email: str):
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(user_email, password)
        server.sendmail(user_email, receiver_email, message)
