import smtplib
from email.message import EmailMessage

from celery import Celery
from config import SMTP_USER, SMTP_PASSWORD

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587

celery = Celery('tasks', broker="redis://localhost:6379")


def get_email_template_msg(username: str):
    email = EmailMessage()
    email['Subject'] = f'Welcome {username}'
    email['From'] = SMTP_USER
    email['To'] = username

    email.set_content(
        f"""
    <h1>Welcome {username}</h1>
    <p>You have been successfully registered.</p>
    """,
        subtype="html",
    )

    return email


# @celery.task(bind=True)
def send_email(username: str):
    email = get_email_template_msg(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
