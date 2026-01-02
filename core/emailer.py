import smtplib, ssl
from email.message import EmailMessage
from typing import Optional
import os

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.strato.de")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER")         # z.B. noreply@tknd-unity-gbr.com
SMTP_PASS = os.getenv("SMTP_PASS")
MAIL_FROM = os.getenv("MAIL_FROM", SMTP_USER)

def send_mail(subject: str, to: str, body: str, attachment: Optional[tuple[str, bytes]] = None):
    if not (SMTP_USER and SMTP_PASS and MAIL_FROM):
        raise RuntimeError("SMTP credentials missing")
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = MAIL_FROM
    msg["To"] = to
    msg.set_content(body)
    if attachment:
        filename, data = attachment
        msg.add_attachment(data, maintype="application", subtype="pdf", filename=filename)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as s:
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)
