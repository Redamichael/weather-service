import smtplib
from email.message import EmailMessage
from datetime import datetime
from .config import *

def send_failure_alert(error_message: str):
    msg = EmailMessage()
    msg["Subject"] = "Weather Service FAILURE Alert"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    msg.set_content(f"""
Weather service failed.

Time: {datetime.now()}

Error:
{error_message}
""")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
