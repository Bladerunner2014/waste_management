from smtplib import SMTP_SSL
from email.message import EmailMessage
from dotenv import dotenv_values
from constants.info_message import InfoMessage
import logging
import json

logger = logging.getLogger("log")
config = dotenv_values(".env")


def send_mail(contacts):
    msg = EmailMessage()
    contacts = json.dumps(contacts)

    logger.info(contacts)
    msg["From"] = config["EMAIL_SENDER"]
    msg["Subject"] = "New ticket!!!"
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           {}
        </p>
      </body>
    </html>
    """
    with SMTP_SSL(config["EMAIL_SERVER"], int(config["PORT"])) as smtp:
        msg.add_alternative(html.format(contacts), subtype="html")
        smtp.login(config["EMAIL_SENDER"], config["PASSWORD"])
        smtp.send_message(msg, to_addrs=config["ADMIN_EMAIL"])
    logger.info(InfoMessage.EMAIL)

    pass
